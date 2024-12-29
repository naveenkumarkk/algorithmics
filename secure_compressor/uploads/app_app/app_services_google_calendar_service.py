# google_calendar_service.py

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_google_calendar_event(user_google_token, event_data):
    """Create a calendar event using the user's Google Calendar."""
    creds = Credentials(token=user_google_token)
    service = build('calendar', 'v3', credentials=creds)
    
    try:
        event = service.events().insert(calendarId='primary', body=event_data).execute()
        return event
    except Exception as e:
        raise Exception(f"Error creating calendar event: {str(e)}")
