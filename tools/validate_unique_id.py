import os
import requests
import uuid
from dotenv import load_dotenv
from pydantic import (BaseModel, Field, EmailStr)
from typing import Optional

# Cargar variables de entorno
load_dotenv()

# Obtener las variables de entorno con validación
MS_COMPANY_B_GET_INFO_URL = os.getenv('MS_COMPANY_B_GET_INFO_URL')
if not MS_COMPANY_B_GET_INFO_URL:
    raise ValueError("MS_COMPANY_B_GET_INFO_URL no está configurada.")
class BusinessData(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del negocio")
    owner_name: str = Field(..., min_length=1, max_length=100, description="Nombre del propietario")
    email: EmailStr = Field(..., description="Correo electrónico válido del propietario")
    address: Optional[str] = Field(None, max_length=250, description="Dirección del negocio (opcional)")
    phone_number: Optional[str] = Field(None, pattern=r"^\+?[0-9]{7,15}$", description="Número de teléfono (opcional)")
    notes: Optional[str] = Field(None, max_length=500, description="Notas adicionales (opcional)")

def fetch_data_from_endpoint(endpoint: str):
    """
    Realiza una solicitud GET a un endpoint específico y retorna los datos en formato JSON.
    
    Parámetros:
    -----------
    endpoint : str
        URL completa del endpoint al que se hará la solicitud.
    
    Retorno:
    --------
    list
        Lista de datos obtenidos del endpoint.
    
    Excepciones:
    ------------
    RuntimeError:
        Si ocurre un error al realizar la solicitud o al procesar la respuesta.
    """
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Eleva una excepción para errores HTTP
        data = response.json()
        if not isinstance(data, list):
            raise ValueError("El formato de respuesta no es una lista.")
        return data
    except Exception as e:
        raise RuntimeError(f"Error al obtener datos del endpoint {endpoint}") from e

def get_all_companies_id():
    """
    Obtiene todos los IDs de los negocios desde el microservicio.
    
    Retorno:
    --------
    list
        Lista de IDs de los negocios.
    """
    endpoint = f"{MS_COMPANY_B_GET_INFO_URL}/get-all-companies-id"
    data = fetch_data_from_endpoint(endpoint)
    return [item.get('id') for item in data]
    
def get_all_branches_id():
    """
    Obtiene todos los IDs de las sucursales desde el microservicio.
    
    Retorno:
    --------
    list
        Lista de IDs de las sucursales.
    """
    endpoint = f"{MS_COMPANY_B_GET_INFO_URL}/get-all-branches-id"
    data = fetch_data_from_endpoint(endpoint)
    return [item.get('id') for item in data]
    
def get_all_companies_et_branches_id():
    """
    Obtiene todos los IDs de negocios y sucursales desde el microservicio.
    
    Retorno:
    --------
    list
        Lista de IDs de negocios y sucursales.
    """
    endpoint = f"{MS_COMPANY_B_GET_INFO_URL}/get-all-companies-et-branches-id"
    data = fetch_data_from_endpoint(endpoint)
    return [item.get('id') for item in data]
    
def generate_unique_company_id(savannah=None, query_the_db=False):
    """
    Genera un ID único para un negocio.
    
    Parámetros:
    -----------
    savannah : list, opcional
        Lista de IDs existentes para evitar duplicados.
    query_the_db : bool, opcional
        Si es True, consulta los IDs existentes en la base de datos.
    
    Retorno:
    --------
    str
        Un ID único generado.
    """
    existing_ids = []
    if query_the_db:
        existing_ids = get_all_branches_id()
    elif savannah:
        existing_ids = savannah
    else:
        raise ValueError("Debe proporcionarse 'savannah' o habilitar 'query_the_db'.")

    existing_ids_set = set(existing_ids)
    unique_id = str(uuid.uuid4())
    while unique_id in existing_ids_set:
        unique_id = str(uuid.uuid4())
    return unique_id
    
def generate_unique_branch_id(savannah=None, query_the_db=False):
    """
    Genera un ID único para una sucursal.
    
    Parámetros:
    -----------
    savannah : list, opcional
        Lista de IDs existentes para evitar duplicados.
    query_the_db : bool, opcional
        Si es True, consulta los IDs existentes en la base de datos.
    
    Retorno:
    --------
    str
        Un ID único generado.
    """
    return generate_unique_company_id(savannah=savannah, query_the_db=query_the_db)
    
def generate_unique_branch_ids(existing_branch_ids, new_branches):
    """
    Genera IDs únicos para una lista de nuevas sucursales.
    
    Parámetros:
    -----------
    existing_branch_ids : list
        Lista de IDs de sucursales existentes.
    new_branches : list
        Lista de sucursales nuevas, cada una representada como un diccionario.
    
    Retorno:
    --------
    list
        Lista de sucursales nuevas con IDs únicos asignados.
    """
    try:
        unique_branches = []
        for branch in new_branches:
            branch_id = str(uuid.uuid4())
            while branch_id in existing_branch_ids:
                branch_id = str(uuid.uuid4())
            unique_branches.append({**branch, 'branch_id': branch_id})
        return unique_branches
    except Exception as e:
        raise RuntimeError('No se pudieron generar los IDs únicos para las sucursales') from e