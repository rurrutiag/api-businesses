import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener las variables de entorno
MS_COMPANY_B_GET_INFO_URL = os.getenv('MS_COMPANY_B_GET_INFO_URL')
if not MS_COMPANY_B_GET_INFO_URL:
    raise EnvironmentError("La variable de entorno 'MS_COMPANY_B_GET_INFO_URL' no está definida.")

def get_company_space_data(company_id):
    """
    Obtiene la información a mostrar en el portal público del negocio.
    Args:
        company_id (uuid.UUID): El ID del negocio en formato UUID
    Returns:
        dict: los datos estructurados del negocio
    """
    try:
        end_point = f"{MS_COMPANY_B_GET_INFO_URL}/get-company-data/{company_id}"
        response = requests.get(end_point)
        response.raise_for_status()
        data = response.json()
        required_keys = ["id", "fantasy_name", "legal_info", "url_domain", "industrial"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing key: {key}")
        company_data = {
            "general": {
                "id": data["id"],
                "fantasy_name": data["fantasy_name"],
                "legal_info": data["legal_info"],
                "url_domain": data["url_domain"],
                "idustrial": data["industrial"],
            },
            "head_quarter": data["head_quarter"],
            "branches": data["branches"],
            "modules": data["modules"],
        }
        return company_data
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Error al obtener los datos del negocio") from e