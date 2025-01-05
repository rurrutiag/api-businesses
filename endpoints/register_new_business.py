import uuid
import os
import requests
from dotenv import load_dotenv
from flask import jsonify
from pydantic import (BaseModel, ValidationError, Field)
from tools.validate_unique_id import (
    generate_unique_branch_ids,
    generate_unique_company_id,
    get_all_companies_et_branches_id)

# Cargar variables de entorno
load_dotenv()

# Obtener las variables de entorno
MS_COMPANY_B_CONFIG_BUSINESS_URL = os.getenv('MS_COMPANY_B_CONFIG_BUSINESS_URL')
if not MS_COMPANY_B_CONFIG_BUSINESS_URL:
    raise ValueError("MS_COMPANY_B_CONFIG_BUSINESS_URL no está configurada.")

class BusinessInput(BaseModel):
    fantasy_name: str = Field(..., description="Nombre de fantasía del negocio")
    legal_info: str = Field(..., description="Información legal del negocio")
    url_domain: str = Field(default="", description="Dominio del negocio")
    industrial: list = Field(default_factory=list, description="Lista de sectores industriales")
    head_quarter: dict = Field(default_factory=dict, description="Información de la sede principal")
    branches: list = Field(default_factory=list, description="Lista de sucursales")
    modules: dict = Field(default_factory=dict, description="Módulos habilitados para el negocio")

def register_new_business(input_data):
    """
    Registra un nuevo negocio utilizando un microservicio.
    
    Parámetros:
    -----------
    input_data : dict
        Datos del negocio que se desean registrar. Deben incluir los campos:
        - fantasy_name: Nombre de fantasía del negocio.
        - legal_info: Información legal del negocio.
        - url_domain (opcional): Dominio del negocio.
        - industrial (opcional): Lista de sectores industriales.
        - head_quarter (opcional): Información de la sede principal.
        - branches (opcional): Lista de sucursales.
        - modules (opcional): Módulos habilitados para el negocio.
    
    Retorno:
    --------
    Response:
        Respuesta en formato JSON con el resultado de la operación.
    """
    
    # required_fields = ['fantasy_name', 'legal_info']
    # for field in required_fields:
    #     if not input_data.get(field):
    #         return jsonify({"message": f"'{field}' es requerido."}), 400

    # try:
    #     # Validar la estructura de los datos de entrada
    #     validated_data = BusinessInput(**input_data)
    # except ValidationError as e:
    #     return jsonify({"message": "Datos de entrada inválidos.", "errors": e.errors()}), 400

    try:
        # 0. Crear variables independientes con los datos rescatados desde input_data
        validated_data = {
            'fantasy_name' : input_data.get('fantasy_name'),
            'legal_info' : input_data.get('legal_info'),
            'url_domain' : input_data.get('url_domain', ""),
            'industrial' : input_data.get('industrial', []),
            'head_quarter' : input_data.get('head_quarter', {}),
            'branches' : input_data.get('branches', []),
            'modules' : input_data.get('modules', {})
        }
        # fantasy_name = input_data.get('fantasy_name')
        # legal_info = input_data.get('legal_info')
        # url_domain = input_data.get('url_domain', "")
        # industrial = input_data.get('industrial', [])
        # head_quarter = input_data.get('head_quarter', {})
        # branches = input_data.get('branches', [])
        # modules = input_data.get('modules', {})

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
        if len(validated_data.branches) > 0:
            formatted_branches = generate_unique_branch_ids(
                existing_branch_ids=existing_branch_ids,
                new_branches=validated_data.branches
            )
        
        # 4. Asegurar que la sede principal también tenga un ID único
        formatted_branches.append({
            'branch_id': head_quarter_id,
            'is_hq': True,
            'is_visible': False,
            **validated_data.head_quarter
        })

        # 5. Agregar el ID único al head_quarter
        enriched_head_quarter = {**validated_data.head_quarter, 'id': head_quarter_id}

        # 6. Construir el objeto de negocio
        payload = {
            'id': register_id,
            'fantasy_name': validated_data.fantasy_name,
            'legal_info': validated_data.legal_info,
            'url_domain': validated_data.url_domain,
            'industrial': validated_data.industrial,
            'head_quarter': enriched_head_quarter,
            'branches': formatted_branches,
            'modules': validated_data.modules
        }

        # 7. Registrar el nuevo negocio en el microservicio
        endpoint_register_new_business = f"{MS_COMPANY_B_CONFIG_BUSINESS_URL}/register-new-business"
        ms_response = requests.post(endpoint_register_new_business, json=payload)

        if ms_response.status_code != 201:
            return jsonify({
                "message": "Error al registrar el negocio en el microservicio.",
                "error": ms_response.text
            }), ms_response.status_code

        # Si la respuesta es exitosa, retornar los datos
        return jsonify({ 'success': True, 'data': ms_response.json()}), 201
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return jsonify({"message": "Ocurrió un error inesperado.", "error": str(e)}), 500
