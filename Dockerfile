# Usa una imagen base de Python
FROM python:3.9-slim

EXPOSE 80

# Define el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "app.py"]