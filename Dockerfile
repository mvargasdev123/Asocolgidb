# 1. Elegimos una versión de Linux súper ligera que ya trae Python 3.11 instalado
FROM python:3.11-slim

# 2. Le decimos a Linux que no genere archivos basura de caché de Python (.pyc)
ENV PYTHONDONTWRITEBYTECODE=1
# Y que escupa los logs directamente en la consola sin demoras
ENV PYTHONUNBUFFERED=1

# 3. Creamos una carpeta de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos ÚNICAMENTE la lista de dependencias primero
# Esto es un truco maestro de caché: si no cambias el requirements.txt, 
# Docker no volverá a descargar todo desde internet la próxima vez.
COPY requirements.txt .

# 5. Instalamos las herramientas.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Ahora sí, copiamos todo nuestro código limpio a la carpeta /app
COPY . .

# 7. Exponemos el puerto 8000 para que el mundo exterior pueda tocar la puerta
EXPOSE 8000

# 8. La orden de ejecución. Arrancamos Uvicorn (el motor detrás de FastAPI) en modo producción.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]