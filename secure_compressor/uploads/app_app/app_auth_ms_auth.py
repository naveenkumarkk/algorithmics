import os
import msal
import requests
from flask import Blueprint, redirect, request, session, url_for, jsonify
from config import Config
from models import User, db
from utils import save_token

ms_bp = Blueprint('ms_bp', __name__)

# Create MSAL confidential client
msal_client = msal.ConfidentialClientApplication(
    Config.MS_CLIENT_ID,
    client_credential=Config.MS_CLIENT_SECRET,
    authority=Config.MS_AUTHORITY
)

@ms_bp.route('/login')
def ms_login():
    # Get the authorization request URL
    auth_url = msal_client.get_authorization_request_url(Config.MS_SCOPE, redirect_uri=Config.MS_REDIRECT_URI)
    return redirect(auth_url)

@ms_bp.route('/callback')
def ms_auth_callback():
    code = request.args.get('code')

    result = msal_client.acquire_token_by_authorization_code(code, scopes=Config.MS_SCOPE, redirect_uri=Config.MS_REDIRECT_URI)

    if "error" in result:
        return jsonify({"error": result.get("error"), "error_description": result.get("error_description")})

    user_info = ms_get_user_info(result['access_token'])
    user = User.query.filter_by(email=user_info['userPrincipalName']).first()
    if not user:
        user = User(email=user_info['userPrincipalName'])
        db.session.add(user)

    user.microsoft_token = result['access_token']
    db.session.commit()

    return jsonify({"message": "Microsoft authentication successful", "user": user.email})

def ms_get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    return response.json()

def get_microsoft_todo_service(user_ms_token):
    # Add MSAL library integration to handle Microsoft ToDo tasks
    pass