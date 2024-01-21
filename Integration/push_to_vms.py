import requests

def send_match_data_to_vms(match_data):
    # Extract relevant information from the FRS webhook data
    matched_lists = match_data["face_events"]["matched_lists"]
    camera_groups = match_data["face_events"]["camera_groups"]
    matched = match_data["face_events"]["matched"]

    # Check if there is a match
    if matched and matched_lists:
        # Assuming you have the details of the matched person, replace this with your actual data
        matched_person_name = "Mak Taylor"

        # Prepare payload for VMS
        vms_payload = {
            "EventName": "Face_Detected_Event",
            "DeviceId": camera_groups[0],  # Assuming there is only one camera group in the webhook data
            "DeviceName": f"CameraGroup_{camera_groups[0]}",  # Modify as needed
            "Properties": {
                "name": matched_person_name
            }
        }

        # URL of the VMS handler
        vms_handler_url = "https://your-vms-endpoint.com/handler"

        # Make a POST request to the VMS handler
        try:
            response = requests.post(vms_handler_url, json=vms_payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print("Match data sent to VMS successfully")
        except requests.exceptions.RequestException as e:
            print(f"Error sending match data to VMS: {e}")

# Example usage with your provided webhook data
frs_webhook_data = {
    "face_events": {
        "matched_lists": [340],
        "camera_groups": [1],
        "matched": True
    }
}

send_match_data_to_vms(frs_webhook_data)
