FROM python:3.9-slim

# Definir una variable de entorno para la dirección IP
ENV SERVER_IP="0.0.0.0"

# Instalar utilidades de internet
RUN apt-get update && apt-get install -y iputils-ping

# Establecer el directorio de trabajo en la imagen
WORKDIR /app

# Copiar el archivo requirements.txt al directorio de trabajo en la imagen
COPY requirements.txt .

# Instalar las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el archivo server.py desde el directorio src al directorio de trabajo en la imagen
COPY src/Server.py .

# Exponer el puerto 5000 para que sea accesible desde fuera del contenedor
EXPOSE 5000

# Establecer el comando predeterminado a ejecutar cuando se inicie el contenedor
CMD ["python", "Server.py"]
