import os
import gzip
import subprocess
from datetime import datetime, timezone, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import FileResponse, Http404

# Zona horaria Colombia (UTC-5)
TZ_BOGOTA = timezone(timedelta(hours=-5))

# Carpeta donde se guardarán los backups localmente
BACKUPS_DIR = os.path.join(settings.BASE_DIR, 'backups_locales')

# ──────────────────────────────────────────
#  Historial de backups locales
# ──────────────────────────────────────────

def _listar_backups_locales():
    """
    Lee la carpeta BACKUPS_DIR y devuelve una lista de los archivos .gz
    ordenados del más reciente al más antiguo.
    """
    archivos = []
    if not os.path.exists(BACKUPS_DIR):
        return archivos

    for filename in os.listdir(BACKUPS_DIR):
        if filename.endswith('.gz'):
            filepath = os.path.join(BACKUPS_DIR, filename)
            stats = os.stat(filepath)
            
            # Formatear tamaño
            size_bytes = stats.st_size
            if size_bytes >= 1_048_576:
                size_str = f"{size_bytes / 1_048_576:.2f} MB"
            elif size_bytes >= 1_024:
                size_str = f"{size_bytes / 1_024:.1f} KB"
            else:
                size_str = f"{size_bytes} B"

            # Formatear fecha de creación
            dt_utc = datetime.fromtimestamp(stats.st_ctime, tz=timezone.utc)
            dt_col = dt_utc.astimezone(TZ_BOGOTA)
            created_str = dt_col.strftime("%d/%m/%Y  %H:%M")

            archivos.append({
                'name': filename,
                'size': size_str,
                'created_time': created_str,
                'timestamp': stats.st_ctime # Para ordenar
            })

    # Ordenar del más nuevo al más viejo
    archivos.sort(key=lambda x: x['timestamp'], reverse=True)
    return archivos


# ──────────────────────────────────────────
#  Vista principal: generar backup
# ──────────────────────────────────────────

def realizar_copia_seguridad(request):
    if request.method == "POST":
        db_config = settings.DATABASES['default']
        db_host = db_config.get('HOST', 'db') or 'db'

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nombre_final = f"backup_sara_{timestamp}.gz"

        # Asegurarnos de que la carpeta existe
        os.makedirs(BACKUPS_DIR, exist_ok=True)

        ruta_sql = os.path.join(BACKUPS_DIR, "backup_temp.sql")
        ruta_gz  = os.path.join(BACKUPS_DIR, nombre_final)

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

            # Paso 2: comprimir directamente en la carpeta final
            with open(ruta_sql, 'rb') as f_in:
                with gzip.open(ruta_gz, 'wb') as f_out:
                    f_out.write(f_in.read())

            messages.success(request, "¡Copia de seguridad generada y guardada exitosamente en el servidor local!")

        except Exception as e:
            messages.error(request, f"Error al generar backup: {str(e)}")

        finally:
            # Limpiamos el .sql temporal, pero DEJAMOS el .gz final
            if os.path.exists(ruta_sql):
                os.remove(ruta_sql)

        return redirect('backups:generar_backup')

    # ── GET: listar historial ──
    backups_historial = _listar_backups_locales()

    return render(request, 'modulos/backups/backups.html', {
        'backups_historial': backups_historial,
    })


# ──────────────────────────────────────────
#  Vista: restaurar backup
# ──────────────────────────────────────────
# (Esta vista se queda casi igual, ya que funciona perfectamente con la subida del archivo)

def restaurar_backup(request):
    if request.method == "POST" and request.FILES.get('archivo_backup'):
        archivo_subido = request.FILES['archivo_backup']

        if archivo_subido.size < 100 or not archivo_subido.name.endswith('.gz'):
            messages.error(request, "Archivo inválido. Asegúrate de subir un backup .gz generado por el sistema.")
            return redirect('backups:generar_backup')

        db_config = settings.DATABASES['default']
        db_host   = db_config.get('HOST', 'db') or 'db'

        CARPETA_TEMP = os.path.join(settings.BASE_DIR, 'backups_locales', 'temp')
        os.makedirs(CARPETA_TEMP, exist_ok=True)

        ruta_gz  = os.path.join(CARPETA_TEMP, "restore_temp.gz")
        ruta_sql = os.path.join(CARPETA_TEMP, "restore_temp.sql")

        try:
            with open(ruta_gz, 'wb+') as destination:
                for chunk in archivo_subido.chunks():
                    destination.write(chunk)

            try:
                with gzip.open(ruta_gz, 'rb') as f_in:
                    contenido = f_in.read()
            except Exception:
                raise Exception("El archivo .gz está corrupto.")

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

            with open(ruta_sql, 'r') as sql_file:
                result = subprocess.run(cmd_restore, stdin=sql_file, stderr=subprocess.PIPE, env=env)

            if result.returncode != 0:
                raise Exception(f"Error al inyectar datos: {result.stderr.decode()}")

            messages.success(request, "¡Base de datos restaurada correctamente!")

        except Exception as e:
            messages.error(request, f"Error crítico al restaurar: {str(e)}")

        finally:
            for f in [ruta_gz, ruta_sql]:
                if os.path.exists(f):
                    os.remove(f)

    return redirect('backups:generar_backup')


# ──────────────────────────────────────────
#  NUEVA VISTA: Descargar Backup Local
# ──────────────────────────────────────────
def descargar_backup(request, nombre_archivo):
    """Permite al usuario descargar el backup desde la tabla de historial"""
    # Seguridad: Evita que descarguen otros archivos del sistema
    if ".." in nombre_archivo or not nombre_archivo.endswith('.gz'):
        raise Http404("Archivo no permitido")

    filepath = os.path.join(BACKUPS_DIR, nombre_archivo)
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=nombre_archivo)
    raise Http404("El archivo no existe en el servidor")