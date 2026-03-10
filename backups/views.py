import os
import json
import gzip
import pickle
import subprocess
from datetime import datetime, timezone, timedelta

# Zona horaria Colombia (UTC-5, sin cambio de horario)
TZ_BOGOTA = timezone(timedelta(hours=-5))

import requests as http_requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_PATH = settings.GOOGLE_DRIVE_TOKEN_PATH
CREDS_PATH = settings.GOOGLE_OAUTH_CREDS_PATH


# ──────────────────────────────────────────
#  Helpers de credenciales
# ──────────────────────────────────────────

def _get_credentials():
    if not os.path.exists(TOKEN_PATH):
        return None
    with open(TOKEN_PATH, 'rb') as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, 'wb') as f:
            pickle.dump(creds, f)
    return creds if creds.valid else None


def _esta_autenticado():
    return _get_credentials() is not None


# ──────────────────────────────────────────
#  Historial de backups desde Google Drive
# ──────────────────────────────────────────

def _listar_backups_drive(creds):
    """
    Devuelve una lista de dicts con info de los archivos de backup
    almacenados en la carpeta de Drive configurada en settings.
    Cada dict contiene: name, size, created_time, web_view_link.
    """
    try:
        service = build('drive', 'v3', credentials=creds)
        query = (
            f"'{settings.GOOGLE_DRIVE_FOLDER_ID}' in parents "
            f"and name contains 'backup_sara' "
            f"and trashed = false"
        )
        results = service.files().list(
            q=query,
            fields="files(id, name, size, createdTime, webViewLink)",
            orderBy="createdTime desc",
            pageSize=50,
        ).execute()

        archivos = []
        for f in results.get('files', []):
            # Formatear tamaño
            size_bytes = int(f.get('size', 0))
            if size_bytes >= 1_048_576:
                size_str = f"{size_bytes / 1_048_576:.2f} MB"
            elif size_bytes >= 1_024:
                size_str = f"{size_bytes / 1_024:.1f} KB"
            else:
                size_str = f"{size_bytes} B"

            # Formatear fecha: Drive devuelve UTC → convertir a hora Colombia (UTC-5)
            created_raw = f.get('createdTime', '')
            try:
                dt_utc = datetime.strptime(created_raw, "%Y-%m-%dT%H:%M:%S.%fZ")
                dt_utc = dt_utc.replace(tzinfo=timezone.utc)
                dt_col = dt_utc.astimezone(TZ_BOGOTA)
                created_str = dt_col.strftime("%d/%m/%Y  %H:%M")
            except Exception:
                created_str = created_raw

            archivos.append({
                'name':          f.get('name', 'Sin nombre'),
                'size':          size_str,
                'created_time':  created_str,
                'web_view_link': f.get('webViewLink', '#'),
            })

        return archivos

    except Exception as e:
        # Si falla silenciosamente devuelve lista vacía; el template lo maneja
        return []


# ──────────────────────────────────────────
#  Vista principal: generar backup
# ──────────────────────────────────────────

def realizar_copia_seguridad(request):
    autenticado = _esta_autenticado()
    creds = _get_credentials()

    if request.method == "POST":
        if not creds:
            return redirect(reverse('backups:google_auth'))

        db_config = settings.DATABASES['default']
        db_host = db_config.get('HOST', 'db') or 'db'

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nombre_final = f"backup_sara_{timestamp}.gz"

        CARPETA_TEMP = os.path.join(settings.BASE_DIR, 'backups', 'temp')
        os.makedirs(CARPETA_TEMP, exist_ok=True)

        ruta_sql = os.path.join(CARPETA_TEMP, "backup_temp.sql")
        ruta_gz  = os.path.join(CARPETA_TEMP, nombre_final)

        try:
            env = os.environ.copy()
            env['MYSQL_PWD'] = str(db_config['PASSWORD'])

            # Paso 1: mysqldump
            cmd_dump = [
                'mysqldump',
                f"-u{db_config['USER']}",
                f"-h{db_host}",
                f"-P{db_config.get('PORT', '3306')}",
                '--add-drop-table',
                '--quick',
                '--protocol=tcp',
                db_config['NAME'],
            ]

            with open(ruta_sql, 'w') as sql_file:
                result = subprocess.run(
                    cmd_dump,
                    stdout=sql_file,
                    stderr=subprocess.PIPE,
                    env=env,
                )

            if result.returncode != 0:
                raise Exception(f"mysqldump falló: {result.stderr.decode()}")
            if os.path.getsize(ruta_sql) < 100:
                raise Exception(f"El dump está vacío. Error: {result.stderr.decode()}")

            # Paso 2: comprimir
            with open(ruta_sql, 'rb') as f_in:
                with gzip.open(ruta_gz, 'wb') as f_out:
                    f_out.write(f_in.read())

            # Paso 3: subir a Drive
            service = build('drive', 'v3', credentials=creds)
            file_metadata = {
                'name':    nombre_final,
                'parents': [settings.GOOGLE_DRIVE_FOLDER_ID],
            }
            media = MediaFileUpload(ruta_gz, mimetype='application/gzip')
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
            ).execute()

            messages.success(request, "¡Copia de seguridad enviada a Google Drive con éxito!")

        except Exception as e:
            messages.error(request, f"Error al generar backup: {str(e)}")

        finally:
            for f in [ruta_sql, ruta_gz]:
                if os.path.exists(f):
                    os.remove(f)

        return redirect('backups:generar_backup')

    # ── GET: listar historial ──
    backups_historial = _listar_backups_drive(creds) if creds else []

    return render(request, 'modulos/backups/backups.html', {
        'autenticado':      autenticado,
        'backups_historial': backups_historial,
    })


# ──────────────────────────────────────────
#  Vista: restaurar backup
# ──────────────────────────────────────────

def restaurar_backup(request):
    if request.method == "POST" and request.FILES.get('archivo_backup'):
        archivo_subido = request.FILES['archivo_backup']

        # ── Validación 1: archivo vacío ──
        if archivo_subido.size == 0:
            messages.error(request, "El archivo está vacío. Selecciona un backup válido.")
            return redirect('backups:generar_backup')

        # ── Validación 2: extensión correcta ──
        if not archivo_subido.name.endswith('.gz'):
            messages.error(request, "El archivo debe tener extensión .gz. Verifica que sea un backup generado por el sistema.")
            return redirect('backups:generar_backup')

        # ── Validación 3: tamaño mínimo razonable (al menos 100 bytes) ──
        if archivo_subido.size < 100:
            messages.error(request, "El archivo es demasiado pequeño para ser un backup válido.")
            return redirect('backups:generar_backup')

        db_config = settings.DATABASES['default']
        db_host   = db_config.get('HOST', 'db') or 'db'

        CARPETA_TEMP = os.path.join(settings.BASE_DIR, 'backups', 'temp')
        os.makedirs(CARPETA_TEMP, exist_ok=True)

        ruta_gz  = os.path.join(CARPETA_TEMP, "restore_temp.gz")
        ruta_sql = os.path.join(CARPETA_TEMP, "restore_temp.sql")

        try:
            with open(ruta_gz, 'wb+') as destination:
                for chunk in archivo_subido.chunks():
                    destination.write(chunk)

            size = os.path.getsize(ruta_gz)
            print(f"[RESTORE] Archivo recibido: {size} bytes")

            # ── Validación 4: verificar que sea un .gz real ──
            if not ruta_gz.endswith('.gz'):
                raise Exception("El archivo no es un Gzip válido.")

            try:
                with gzip.open(ruta_gz, 'rb') as f_in:
                    contenido = f_in.read()
            except (gzip.BadGzipFile, OSError, EOFError):
                raise Exception("El archivo .gz está corrupto o no es un backup válido generado por el sistema.")

            print(f"[RESTORE] SQL descomprimido: {len(contenido)} bytes")

            # ── Validación 5: contenido SQL mínimo ──
            if len(contenido) < 100:
                raise Exception("El backup está vacío o corrupto tras descomprimir.")

            with open(ruta_sql, 'wb') as f_out:
                f_out.write(contenido)

            env = os.environ.copy()
            env['MYSQL_PWD'] = str(db_config['PASSWORD'])

            cmd_restore = [
                'mysql',
                f"-u{db_config['USER']}",
                f"-h{db_host}",
                f"-P{db_config.get('PORT', '3306')}",
                '--protocol=tcp',
                db_config['NAME'],
            ]

            print(f"[RESTORE] Ejecutando: {' '.join(cmd_restore)}")

            with open(ruta_sql, 'r') as sql_file:
                result = subprocess.run(
                    cmd_restore,
                    stdin=sql_file,
                    stderr=subprocess.PIPE,
                    env=env,
                )

            print(f"[RESTORE] Return code: {result.returncode}")
            print(f"[RESTORE] Stderr: {result.stderr.decode()}")

            if result.returncode != 0:
                raise Exception(f"mysql falló: {result.stderr.decode()}")

            messages.success(request, "¡Base de datos restaurada correctamente!")

        except Exception as e:
            print(f"[RESTORE] Excepción: {str(e)}")
            messages.error(request, f"Error crítico: {str(e)}")

        finally:
            for f in [ruta_gz, ruta_sql]:
                if os.path.exists(f):
                    os.remove(f)

    return redirect('backups:generar_backup')


# ──────────────────────────────────────────
#  Vistas OAuth Google
# ──────────────────────────────────────────

def google_auth(request):
    with open(CREDS_PATH, 'r') as f:
        creds_data = json.load(f)

    client_info = creds_data.get('installed') or creds_data.get('web')
    client_id   = client_info['client_id']
    redirect_uri = request.build_absolute_uri(reverse('backups:google_callback'))
    request.session['redirect_uri'] = redirect_uri

    import urllib.parse
    params = {
        'client_id':     client_id,
        'redirect_uri':  redirect_uri,
        'response_type': 'code',
        'scope':         ' '.join(SCOPES),
        'access_type':   'offline',
        'prompt':        'consent',
    }
    auth_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params)
    return redirect(auth_url)


def google_callback(request):
    code         = request.GET.get('code')
    redirect_uri = request.session.get('redirect_uri')

    if not code:
        messages.error(request, "No se recibió código de autorización de Google.")
        return redirect('backups:generar_backup')

    with open(CREDS_PATH, 'r') as f:
        creds_data = json.load(f)

    client_info   = creds_data.get('installed') or creds_data.get('web')
    client_id     = client_info['client_id']
    client_secret = client_info['client_secret']
    token_uri     = client_info['token_uri']

    response   = http_requests.post(token_uri, data={
        'code':          code,
        'client_id':     client_id,
        'client_secret': client_secret,
        'redirect_uri':  redirect_uri,
        'grant_type':    'authorization_code',
    })
    token_data = response.json()

    if 'error' in token_data:
        messages.error(
            request,
            f"Error al vincular Google: {token_data.get('error_description', token_data['error'])}"
        )
        return redirect('backups:generar_backup')

    creds = Credentials(
        token=token_data['access_token'],
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_uri,
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )

    with open(TOKEN_PATH, 'wb') as f:
        pickle.dump(creds, f)

    messages.success(request, "Google Drive vinculado correctamente.")
    return redirect('backups:generar_backup')


if settings.DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'