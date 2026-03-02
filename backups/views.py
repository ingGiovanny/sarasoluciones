import os
import pickle
import subprocess
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_PATH = settings.GOOGLE_DRIVE_TOKEN_PATH
CREDS_PATH = settings.GOOGLE_OAUTH_CREDS_PATH


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


def realizar_copia_seguridad(request):
    autenticado = _esta_autenticado()

    if request.method == "POST":
        creds = _get_credentials()
        if not creds:
            return redirect(reverse('backups:google_auth'))

        db_config = settings.DATABASES['default']
        ENCRYPT_PASS = getattr(settings, 'BACKUP_ENCRYPTION_KEY', settings.SECRET_KEY)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nombre_final = f"backup_sara_{timestamp}.sql.gz.enc"

        CARPETA_TEMP = os.path.join(settings.BASE_DIR, 'backups', 'temp')
        os.makedirs(CARPETA_TEMP, exist_ok=True)

        ruta_gz = os.path.join(CARPETA_TEMP, f"{nombre_final}.gz")
        ruta_enc = os.path.join(CARPETA_TEMP, nombre_final)

        try:
            os.environ['MYSQL_PWD'] = str(db_config['PASSWORD'])

            comando_dump = (
                f"mysqldump -u {db_config['USER']} -h {db_config.get('HOST', 'localhost')} "
                f"--add-drop-table --quick {db_config['NAME']} | gzip > {ruta_gz}"
            )
            subprocess.run(comando_dump, shell=True, check=True)

            comando_encrypt = (
                f"openssl enc -aes-256-cbc -salt -in {ruta_gz} -out {ruta_enc} "
                f"-k '{ENCRYPT_PASS}' -pbkdf2"
            )
            subprocess.run(comando_encrypt, shell=True, check=True)

            service = build('drive', 'v3', credentials=creds)
            file_metadata = {
                'name': nombre_final,
                'parents': [settings.GOOGLE_DRIVE_FOLDER_ID]
            }
            media = MediaFileUpload(ruta_enc, mimetype='application/octet-stream')
            service.files().create(
                body=file_metadata, media_body=media, fields='id'
            ).execute()

            messages.success(request, "¡Copia de seguridad enviada a Google Drive con éxito!")

        except Exception as e:
            messages.error(request, f"Error al generar backup: {str(e)}")

        finally:
            for f in [ruta_gz, ruta_enc]:
                if os.path.exists(f):
                    os.remove(f)

        return redirect('backups:generar_backup')

    return render(request, 'backups/backups.html', {'autenticado': autenticado})


def restaurar_backup(request):
    if request.method == "POST" and request.FILES.get('archivo_backup'):
        archivo_subido = request.FILES['archivo_backup']
        db_config = settings.DATABASES['default']
        ENCRYPT_PASS = getattr(settings, 'BACKUP_ENCRYPTION_KEY', settings.SECRET_KEY)

        CARPETA_TEMP = os.path.join(settings.BASE_DIR, 'backups', 'temp')
        os.makedirs(CARPETA_TEMP, exist_ok=True)

        ruta_enc = os.path.join(CARPETA_TEMP, "restore_temp.enc")
        ruta_gz = os.path.join(CARPETA_TEMP, "restore_temp.sql.gz")

        try:
            with open(ruta_enc, 'wb+') as destination:
                for chunk in archivo_subido.chunks():
                    destination.write(chunk)

            cmd_decrypt = (
                f"openssl enc -aes-256-cbc -d -salt -in {ruta_enc} -out {ruta_gz} "
                f"-k '{ENCRYPT_PASS}' -pbkdf2"
            )
            subprocess.run(cmd_decrypt, shell=True, check=True)

            os.environ['MYSQL_PWD'] = str(db_config['PASSWORD'])

            cmd_restore = (
                f"gzip -dc {ruta_gz} | mysql -u {db_config['USER']} "
                f"-h {db_config.get('HOST', 'localhost')} {db_config['NAME']}"
            )
            subprocess.run(cmd_restore, shell=True, check=True, env=os.environ)

            messages.success(request, "¡Base de datos restaurada correctamente!")

        except subprocess.CalledProcessError as e:
            messages.error(request, f"Fallo en la restauración (Status {e.returncode}). Verifica que el archivo sea un backup válido.")
        except Exception as e:
            messages.error(request, f"Error crítico: {str(e)}")

        finally:
            for f in [ruta_enc, ruta_gz]:
                if os.path.exists(f):
                    os.remove(f)

    return redirect('backups:generar_backup')


def google_auth(request):
    flow = Flow.from_client_secrets_file(
        CREDS_PATH, scopes=SCOPES,
        redirect_uri=request.build_absolute_uri(reverse('backups:google_callback'))
    )
    auth_url, state = flow.authorization_url(access_type='offline', prompt='consent')
    request.session['oauth_state'] = state
    return redirect(auth_url)


def google_callback(request):
    state = request.session.get('oauth_state')
    flow = Flow.from_client_secrets_file(
        CREDS_PATH, scopes=SCOPES, state=state,
        redirect_uri=request.build_absolute_uri(reverse('backups:google_callback'))
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    with open(TOKEN_PATH, 'wb') as f:
        pickle.dump(flow.credentials, f)
    messages.success(request, "Google Drive vinculado correctamente.")
    return redirect('backups:generar_backup')


if settings.DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'