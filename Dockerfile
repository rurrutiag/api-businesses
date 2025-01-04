# Usa una imagen base de Python
FROM python:3.9-slim

EXPOSE 8080

# Copia los archivos del proyecto al contenedor
COPY . /app

# Define el directorio de trabajo
WORKDIR /app

EXPOSE 8080

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]