# Usa una imagen base de Python
FROM python:3.9-slim

# Define el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias
# RUN python3 -m venv .venv
# RUN . .venv/bin/activate && pip install --upgrade pip
# RUN . .venv/bin/activate && pip install -r requirements.txt
RUN pip install flask

# Expone el puerto donde correrá la aplicación
EXPOSE 5000

# Comando para correr la aplicación con Gunicorn
# CMD [".venv/bin/gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
CMD ["python", "app.py"]