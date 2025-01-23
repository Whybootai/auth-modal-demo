from flask import Flask, request, jsonify, redirect
import requests
import json

app = Flask(__name__)

CLIENT_ID = '583125721525-95l13p8v8bou7ts0bngalren5pp9i28o.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'https://auth-modal-demo-1.onrender.com/callback'  # Must match the redirect URI in client-side
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
USER_INFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"


@app.route('/exchange-code', methods=['POST'])
def exchange_code():
    data = request.get_json()
    auth_code = data.get('code')

    if not auth_code:
       return jsonify({"error":"Code not provided"}), 400

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    try:
        response = requests.post(TOKEN_ENDPOINT, data=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        token_data = response.json()
        access_token = token_data.get("access_token")
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching token: {str(e)}"}), 500

    if not access_token:
        return jsonify({"error": "No access token returned"}), 500

    user_info = get_user_info(access_token) # function below
    if not user_info:
        return jsonify({"error": "Failed to fetch user data"}), 500


    return jsonify(user_info)

def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(USER_INFO_ENDPOINT, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
         print(f"Error fetching user info: {str(e)}") # print to console to log errors
         return None

@app.route('/callback')
def callback():
    # Handle the redirect. This is where you receive the auth code.
    # You may handle the auth code, exchange it for a token
    # and perform further actions
    return "Successfully received the auth code, server has processed it"

if __name__ == '__main__':
   app.run(debug=True, port=10000)
