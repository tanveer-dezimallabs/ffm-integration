# camera_api.py

import requests

class CameraApiClient:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.base_url = "http://example.com/camera-api"

    def get_camera_name(self, camera_id):
        try:
            url = f"{self.base_url}/camera/{camera_id}"
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                camera_name = response.json().get("name", "")
                return camera_name
            else:
                print(f"Failed to retrieve camera name. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error retrieving camera name: {str(e)}")
            return None
