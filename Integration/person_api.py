import requests

def get_matched_name(matched_card):
    """
    Get the actual name by making a call to the name API with Bearer token.

    Args:
    - matched_card (str): The matched_card value to be used as a parameter.
    - auth_token (str): The authentication token for the Bearer token.

    Returns:
    - str: The actual name retrieved from the API.
    """
    try:
        # Replace the API endpoint with the actual endpoint for retrieving names
        auth_token =  "Token 26e0ea0fa402ba83f0a52b5735ff53e8d12e0ec8fc6db5495495fa98e7671d85"
        name_api_url = f"http://localhost/cards/humans/{matched_card}"
        headers = {'Authorization': f'{auth_token}'}
        
        response = requests.get(name_api_url, headers=headers)

        if response.status_code == 200:
            actual_name = response.json().get("name", "")
            return actual_name
        else:
            print(f"Failed to retrieve name from the name API. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error retrieving name from the name API: {str(e)}")
        return None

# Example usage:
# matched_card = "123456789"
# auth_token = "your_token_here"
# actual_name = get_actual_name(matched_card, auth_token)
# print(actual_name)