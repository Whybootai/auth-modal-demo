from flask import Flask, request, jsonify, redirect
import requests
from urllib.parse import urlencode
import os

app = Flask(__name__)

# OAuth2 credentials loaded from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')  # Ensure this matches in your Google console

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise EnvironmentError("Missing CLIENT_ID, CLIENT_SECRET, or REDIRECT_URI in environment variables.")

# Google OAuth2 endpoints
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'
USER_INFO_ENDPOINT = 'https://www.googleapis.com/oauth2/v3/userinfo'

@app.route('/')
def home():
    # Redirect to Google login
    google_auth_url = get_google_auth_url()
    return redirect(google_auth_url)

def get_google_auth_url():
    # Build the Google OAuth2 authorization URL
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid profile email',
        'access_type': 'offline',
        'include_granted_scopes': 'true',
    }
    auth_url = AUTHORIZATION_URL + '?' + urlencode(params)
    return auth_url

@app.route('/callback')
def callback():
    # Handle the redirect from Google OAuth with the authorization code
    auth_code = request.args.get('code')
    if not auth_code:
        return jsonify({"error": "Authorization code not provided"}), 400

    # Exchange the authorization code for an access token
    token_data = exchange_code_for_token(auth_code)
    if 'error' in token_data:
        return jsonify(token_data), 400

    # Fetch user info using the access token
    user_info = get_user_info(token_data['access_token'])
    if user_info:
        return jsonify(user_info)
    else:
        return jsonify({"error": "Failed to fetch user data"}), 500

def exchange_code_for_token(auth_code):
    # Exchange authorization code for access token
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }

    try:
        response = requests.post(TOKEN_ENDPOINT, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"Error fetching token: {str(e)}"}

def get_user_info(access_token):
    # Fetch the user's Google profile information using the access token
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(USER_INFO_ENDPOINT, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
