import os
import requests

def touch_post_ms(endpoint_url, payload):
    try:
        ms_response = requests.post(endpoint_url, json=payload)
        ms_response.raise_for_status()
        if ms_response.status_code != 201:
            return {
                "message": "Error al ingresar datos.",
                "error": ms_response.text,
                "code": ms_response.status_code
            }
        return ms_response.json()
    except requests.exceptions.RequestException as e:
        return None
    
def send_post_requests_concurrently(endpoint_url, data_list):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(touch_post_ms, endpoint_url, data) for data in data_list
        ]
        results = []
        for future in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})
    return results