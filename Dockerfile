# -----------------------------------------------------------------
# Dockerfile para una aplicación Django
# -----------------------------------------------------------------

# Etapa 1: Imagen Base
FROM python:3.11-slim

# Etapa 2: Variables de Entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Etapa 3: Instalar Dependencias del Sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    gcc \
    libcairo2-dev \
    libpango1.0-dev \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Etapa 4: Configurar el Directorio de Trabajo
WORKDIR /app

# Etapa 5: Instalar Dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Etapa 6: Copiar el Código de la Aplicación
COPY . .

# Etapa 7: Exponer el Puerto
EXPOSE 8000

# Etapa 8: Comando de Ejecución
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

