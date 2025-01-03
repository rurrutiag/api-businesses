import uuid
import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from tools.validate_unique_id import generate_unique_branch_ids, generate_unique_company_id, get_all_companies_et_branches_id

# Cargar variables de entorno
load_dotenv()

# Obtener las variables de entorno
MS_COMPANY_B_CONFIG_BUSINESS_URL = os.getenv('MS_COMPANY_B_CONFIG_BUSINESS_URL').strip()

def register_new_business(input_data):
    
    fantasy_name = input_data.get('fantasy_name')
    legal_info = input_data.get('legal_info')
    url_domain = input_data.get('url_domain', "")
    industrial = input_data.get('industrial', [])
    head_quarter = input_data.get('head_quarter', {})
    branches = input_data.get('branches', [])
    modules = input_data.get('modules', {})

    try:
        # 1. Consultar todos los ids y branch_ids existentes
        existing_data = get_all_companies_et_branches_id()
        existing_company_ids = [company['id'] for company in existing_data]
        existing_branch_ids = [company['branch_ids'] for company in existing_data]

        # 2. Generar el ID único para la compañía y la sede principal
        register_id = generate_unique_company_id(savannah=existing_company_ids, query_the_db=False)
        head_quarter_id = uuid.uuid4().hex
        while head_quarter_id in existing_branch_ids:
            head_quarter_id = uuid.uuid4().hex

        # 3. Generar los branch_ids únicos para las sucursales
        formatted_branches = []
        if len(branches) > 0:
            formatted_branches = generate_unique_branch_ids(existing_branch_ids=existing_branch_ids, new_branches=branches)
        
        # 4. Asegurar que la sede principal también tenga un ID único
        formatted_branches.append({
            'branch_id': head_quarter_id,
            'is_hq': True,
            'is_visible': False,
            **head_quarter
        })

        # 5. Agregar el ID único al head_quarter
        enriched_head_quarter = {**head_quarter, 'id': head_quarter_id}

        # 6. Construir el objeto de negocio
        payload = {
            'id': register_id,
            'fantasy_name': fantasy_name,
            'legal_info': json.dumps(legal_info),
            'url_domain': url_domain,
            'industrial': json.dumps(industrial),
            'head_quarter': json.dumps(enriched_head_quarter),
            'branches': json.dumps(formatted_branches),
            'modules': json.dumps(modules)
        }

        # 7. Registrar el nuevo negocio en el microservicio
        endpoint_register_new_business = f"{MS_COMPANY_B_CONFIG_BUSINESS_URL}/register-new-business"
        ms_response = requests.post(endpoint_register_new_business, json=payload)

        # Si la respuesta es exitosa, retornar los datos
        return jsonify({ 'success': True, 'data': ms_response.json()}), 201
    except Exception as e:
        print(f"Error en el registro de negocio: {str(e)}")
        return jsonify({"message": "Error al registrar el negocio en el microservicio.", "error": str(e)}), 500