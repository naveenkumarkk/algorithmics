# zapier_service.py

import requests

def send_to_zapier(payload):
    """Send data to Zapier when a certain event is triggered."""
    zapier_webhook_url = 'your_zapier_webhook_url'
    try:
        response = requests.post(zapier_webhook_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error sending data to Zapier: {str(e)}")
