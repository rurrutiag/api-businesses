import os
from flask import jsonify
from dotenv import load_dotenv
from tools.communication_with_microservices import (
    touch_post_ms,
    send_post_requests_concurrently
)

# Load environment variables
load_dotenv()

MS_COMPANY_B_CONFIG_BUSINESS_URL = os.getenv('MS_COMPANY_B_CONFIG_BUSINESS_URL')
if not MS_COMPANY_B_CONFIG_BUSINESS_URL:
    raise ValueError("MS_COMPANY_B_CONFIG_BUSINESS_URL no está configurada.")

def handle_process(action, data):
    """
    It processes different actions by associating endpoint
    
    :param action: Action name to realize
    :param data: Necessary data for the action
    :return: Dictionary with process results
    """
    # 0. Set variables with the endpoints urls
    endpoint_setup_branches = f"{MS_COMPANY_B_CONFIG_BUSINESS_URL}/setup-branches"
    endpoint_setup_business_sections = f"{MS_COMPANY_B_CONFIG_BUSINESS_URL}/setup-business-sections"
    endpoint_setup_navigation_section = f"{MS_COMPANY_B_CONFIG_BUSINESS_URL}/setup-navigation-section"
    endpoint_company_belongs_to_industrial_sector = f"{MS_COMPANY_B_CONFIG_BUSINESS_URL}/company-belongs-to-industrial-sector"

    api_response = {}
    try:
        # 1. Is this a request for the branches process?
        if action == "branches":
            branches_results = send_post_requests_concurrently(endpoint_setup_branches, [
                {
                    'company_id': data["company_id"],
                    'name': branch['name'],
                    'is_visible': branch['is_visible'],
                    'is_hq':branch['is_hq'],
                    'address': branch['address']
                } for branch in data["branches"]
            ])
            api_response['results'] = branches_results
        # 2. Is this a request for the business sections process?
        elif action == "business_sections":
            payload = {
                    'company_id': data["company_id"],
                    **data["sections"]
                    # 'page': data["sections"]["page"],
                    # 'order': data["sections"]["order"],
                    # 'component': data["sections"]["component"],
                    # 'component_variant_id': data["sections"]["component_variant_id"],
                    # 'content': data["sections"]["content"],
                    # 'metadata': data["sections"]["metadata"]
                }
            sections_results = touch_post_ms(
                endpoint_url=endpoint_setup_business_sections,
                payload=payload)
            api_response['results'] = sections_results 
        # 3. Is this a request for the navigation process?
        elif action == "navigation_section":
            payload = {
                    'company_id': data["company_id"],
                    **data["navigation"]
                    # 'label': data["navigation"]["label"],
                    # 'link': data["navigation"]["link"],
                    # 'tab': data["navigation"]["tab"],
                    # 'action': data["navigation"]["action"],
                    # 'order_position': data["navigation"]["order_position"],
                    # 'icon': data["navigation"]["icon"]
                }
            navigation_results = touch_post_ms(
                endpoint_url=endpoint_setup_navigation_section,
                payload=payload)
            api_response['results'] = navigation_results
        # 4. Is this a request for the industrial sector process?
        if action == "industrial_sector":
            industrial_results = send_post_requests_concurrently(
                endpoint_company_belongs_to_industrial_sector,
                [
                    {
                        'company_id': data["company_id"],
                        'industrial': industrial_sector
                    } for industrial_sector in data["industrial"]
                ]
            )
            api_response['results'] = industrial_results
        return {
            'success': True,
            'data': api_response
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"Error while processing {action}: {str(e)}"
        }

def setup_business(input_data):
    """
    Configure a business, processing different data types

    :param input_data: A dictionary list with data and processes to run.
    :return: JSON response with the status of the operation.
    """
    try:
        # 1. Set API response variable
        api_response = {}

        # 2. Set process options
        expected_values = {
            "branches",
            "business_sections",
            "navigation_section",
            "industrial_sector"
            }
        # 2.1 Verify that array contains a dictionary with 'process' key
        for item in input_data:
            if (
                isinstance(item, dict) and
                "process" in item and
                isinstance(item["process"], str) and
                item["process"] in expected_values
            ):
                # if the key exists, is a string and has a valid value, continue
                return handle_process(action=item["process"], data=input_data)
            else:
                # Setup failed
                return {
                    'success': False,
                    'message': "Process doesn't exist or isn't valid"
                }
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return {
            "success": False,
            "message": "Unexpected error happen.", "error": str(e),
            "error": str(e)
        }