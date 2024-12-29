import json
from flask import session, redirect, url_for
import logging
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def save_token(user, token, provider):
    if provider == 'google':
        user.google_token = json.dumps(token)
    elif provider == 'microsoft':
        user.microsoft_token = json.dumps(token)

def login_required(func):
    def wrapper(*args, **kwargs):
        logging.debug(f"Login Wrapper: {session}")
        if not session.get("google_token"):
            # Redirect to the login page if not logged in
            return redirect(url_for("index"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Preserve the original function's name
    return wrapper
