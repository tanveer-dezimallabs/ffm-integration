from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        # Process the data received from the webhook
        process_webhook_data(data)
        
        # Respond to the webhook request
        return jsonify({'status': 'success'})
    
    except Exception as e:
        # Handle any exceptions or errors
        return jsonify({'status': 'error', 'message': str(e)})
    
import requests
import base64

def download_and_encode_image(image_url):
    """
    Download an image from the given URL and encode it as base64.

    Args:
    - image_url (str): The URL of the image to download.

    Returns:
    - str: The base64-encoded string representing the image.
    """
    response = requests.get(image_url)
    
    if response.status_code == 200:
        image_binary = response.content
        image_base64 = base64.b64encode(image_binary).decode('utf-8')
        return image_base64
    else:
        print(f"Failed to download image from {image_url}. Status code: {response.status_code}")
        return None

def process_webhook_data(data):
    try:
        # Check if data is a list and has at least one item
        if isinstance(data, list) and len(data) > 0:
            # Access each item in the list
            for data_item in data:
                # Extract relevant information from the payload
                card_id = data_item.get("matched_card", "")
                snapshot_url = data_item.get("thumbnail", "")
                camera_id = data_item.get("camera", "")
                # Download and encode the image
                snapshot_base64 = download_and_encode_image(snapshot_url)
                matched_person_name = get_matched_name(card_id)
                camera_name  = get_camera_name(camera_id)

                if snapshot_base64 is not None:
                    # Create a new payload for the POST request
                    payload = {
                        "EventName": "Face_Detected_Event",  # Hardcoded
                        "DeviceId": 2,  # Hardcoded
                        "Snapshot": snapshot_base64,
                        "Properties": {
                            "Name": matched_person_name,
                            "Camera Name" : camera_name
                        }
                    }

                    # Send the data to another location using a POST request
                    post_api_url = "http://172.17.0.10:8800/RestService/server/GenerateEvent"  
                    response = requests.post(post_api_url, json=payload)

                    # Check the response status
                    if response.status_code == 200:
                        print("Data sent successfully to another location.")
                    else:
                        print(f"Failed to send data. Status code: {response.status_code}")

        else:
            print("Invalid data format received. Expected a list with at least one item.")

    except Exception as e:
        # Handle any exceptions or errors
        print(f"Error processing webhook data: {str(e)}")


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
    
import requests

def get_camera_name(cameraid):
    try:
        # Replace the API endpoint with the actual endpoint for retrieving names
        auth_token =  "Token 26e0ea0fa402ba83f0a52b5735ff53e8d12e0ec8fc6db5495495fa98e7671d85"
        name_api_url = f"http://localhost/cameras/{cameraid}"
        headers = {'Authorization': f'{auth_token}'}
        
        response = requests.get(name_api_url, headers=headers)

        if response.status_code == 200:
            camera_name = response.json().get("name", "")
            return camera_name
        else:
            print(f"Failed to retrieve camera name from the API. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error retrieving name from the name API: {str(e)}")
        return None


if __name__ == '__main__':
    # Start the Flask web server on port 5000 (you can change it to any available port)
    app.run(port=5000)
