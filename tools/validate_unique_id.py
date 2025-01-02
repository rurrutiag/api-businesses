import os
import requests
import uuid
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener las variables de entorno
MS_COMPANY_B_GET_INFO_URL = os.getenv('MS_COMPANY_B_GET_INFO_URL').strip()

def get_all_companies_id():
    """Obtiene todos los IDs de los negocios desde el microservicio."""
    try:
        end_point = f"{MS_COMPANY_B_GET_INFO_URL}/get-all-companies-id"
        response = requests.get(end_point)
        response.raise_for_status() # Levanta excepciones para errores HTTP
        data = response.json()
        existing_ids = [item['id'].strip() for item in data]
        return existing_ids
    except Exception as e:
        raise RuntimeError('No se pudieron obtener los IDs existentes') from e
    
def get_all_branches_id():
    """Obtiene todos los IDs de las sucursales desde el microservicio."""
    try:
        end_point = f"{MS_COMPANY_B_GET_INFO_URL}/get-all-branches-id"
        response = requests.get(end_point)
        response.raise_for_status()
        data = response.json()
        existing_ids = [item['id'].strip() for item in data]
        return existing_ids
    except Exception as e:
        raise RuntimeError('No se pudieron obtener los IDs existentes') from e
    
def get_all_companies_et_branches_id():
    """Obtiene todos los IDs de negocios y sucursales desde el microservicio."""
    try:
        end_point = f"{MS_COMPANY_B_GET_INFO_URL}/get-all-companies-et-branches-id"
        response = requests.get(end_point)
        response.raise_for_status()
        data = response.json()
        existing_ids = [item['id'].strip() for item in data]
        return existing_ids
    except Exception as e:
        raise RuntimeError('No se pudieron obtener los IDs existentes') from e
    
def generate_unique_company_id(savannah=None, query_the_db=False):
    """Genera un ID único para un negocio"""
    try:
        existing_ids = []
        if query_the_db:
            existing_ids = get_all_branches_id()
        elif savannah:
            existing_ids = savannah
        else:
            raise ValueError('Inconsistencia: no se solicita query y no se entrega sabana de datos')
    
        existing_ids_set = set(existing_ids)
        unique_id = str(uuid.uuid4())
        while unique_id in existing_ids_set:
            unique_id = str(uuid.uuid4())
        return unique_id
    except Exception as e:
        raise RuntimeError('No se pudo generar el ID único') from e
    
def generate_unique_branch_id(savannah=None, query_the_db=False):
    """Genera un ID único para una sucursal."""
    try:
        existing_ids = []
        if query_the_db:
            existing_ids = get_all_branches_id()
        elif savannah:
            existing_ids = savannah
        else:
            raise ValueError('Inconsistencia: no se solicita query y no se entrega sabana de datos')

        existing_ids_set = set(existing_ids)
        unique_id = str(uuid.uuid4())
        while unique_id in existing_ids_set:
            unique_id = str(uuid.uuid4())
        return unique_id
    except Exception as e:
        raise RuntimeError('No se pudo generar el ID único') from e
    
def generate_unique_branch_ids(existing_branch_ids, new_branches):
    """Genera IDs únicos para una lista de nuevas sucursales."""
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