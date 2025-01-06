from flask import (Flask, jsonify, request, send_from_directory, redirect)
from flask_cors import CORS
from dotenv import load_dotenv
import uuid
load_dotenv()

import os

from endpoints.get_company_data import get_company_space_data
from endpoints.register_new_business import register_new_business

cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": cors_origins if cors_origins else "*", # Si no se define, permitir todos los orígenes
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/')
def home():
    return send_from_directory('static','index.html')

@app.errorhandler(404)
def not_found(e):
    return redirect('/'), 404

@app.route('/get-company-space-data/<id>', methods=['GET'])
def get_company_space_data_route(id):
    try:
        company_id = id
        company_data = get_company_space_data(company_id)
        return jsonify(company_data), 200
    except RuntimeError as e:
        return jsonify({"message": "Error al capturar datos", "error": str(e)}), 500

@app.route('/register-new-business', methods=['POST'])
def register_new_business_route():
    input_data = request.json
    if not input_data:
        return jsonify({"message": "El cuerpo de la solicitud está vacío o no es JSON válido."}), 400
    try:
        new_business_data = register_new_business(input_data)
        return jsonify(new_business_data), 200
    except RuntimeError as e:
        return jsonify({"message": "Error al registrar el negocio en el microservicio.", "error": str(e)}), 500

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, port=8080)
