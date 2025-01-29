import os
from dotenv import load_dotenv
from flask import jsonify
from tools.communication_with_microservices import (
    touch_post_ms
)

# Load environment variables
load_dotenv()

# Get environments variables
MS_COMPANY_B_CONFIG_BUSINESS_URL = os.getenv('MS_COMPANY_B_CONFIG_BUSINESS_URL')
if not MS_COMPANY_B_CONFIG_BUSINESS_URL:
    raise ValueError("MS_COMPANY_B_CONFIG_BUSINESS_URL no está configurada.")

def register_new_business(input_data):
    """
    Register a new business.
    
    Parameters:
    -----------
    input_data : dict
        Business data to be registered. Must include the following fields:
        - fantasy_name: Fantasy name of the business (to consumers).
        - legal_info: Legal information of the business (A.K.A.: Unique tax role, among others).
        - url_domain (opcional): w3 business domain.    
    Return:
    --------
    Response:
        JSON response with operation results, include company ID.
    """
    
    try:
        # 0. Set array with request data from input_data
        validated_data = {
            'fantasy_name' : input_data.get('fantasy_name'),
            'legal_info' : input_data.get('legal_info'),
            'url_domain' : input_data.get('url_domain', "")
        }
      
        # 1. Set variables with the endpoint urls
        endpoint_register_new_company = f"{MS_COMPANY_B_CONFIG_BUSINESS_URL}/register-new-company"
        
        # 2. Set Api response variable
        api_response = {}

        # 3. Create the company in the database
        payload = {
            'fantasy_name': validated_data['fantasy_name'],
            'legal_info': validated_data['legal_info'],
            'url_domain': validated_data['url_domain']
        }
        
        ms_register_new_company = touch_post_ms(endpoint_url=endpoint_register_new_company, payload=payload)
        
        if not ms_register_new_company or 'company_id' not in ms_register_new_company:
            return {'error': 'Error registering business'}

        # 4 Set identificator string company
        company_id = ms_register_new_company['company_id']
        api_response['results'] = ms_register_new_company

        return {
            'success': True,
            'data': api_response
        }
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return jsonify({"message": "Unexpected error happen", "error": str(e)})
