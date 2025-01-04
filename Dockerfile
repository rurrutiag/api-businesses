# Usa una imagen base de Python
FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./endpoints/ /app/endpoints/
COPY ./app.py /app/

EXPOSE 8080

ENV FLASK_APP=app.py

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]