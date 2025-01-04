# Usa una imagen base de Python
FROM python:3.9-slim

WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY endpoints/ /app/endpoints/
COPY app.py /app/
COPY requirements.txt /app/

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=app.py

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "4"]