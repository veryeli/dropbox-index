from dropbox_config import APP_KEY, APP_SECRET

import requests
import base64


# open the url in a browser and get the user to enter the token
url_for_token = f'https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&response_type=code&token_access_type=offline'
print('please go to this url and enter the code you get back here')
print(url_for_token)
token = input('Enter the code: ')


# Encode your app key and secret for the Authorization header
credentials = f"{APP_KEY}:{APP_SECRET}"
base64_credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')

# Set up the headers
headers = {
    'Authorization': f'Basic {base64_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Set up the form data
data = {
    'code': token,
    'grant_type': 'authorization_code'
}

# Make the POST request to exchange the authorization code for tokens
response = requests.post('https://api.dropbox.com/oauth2/token', headers=headers, data=data)

# Process the response
print('update the following in dropbox_config.py')
if response.status_code == 200:
    tokens = response.json()
    print(f"ACCESS_TOKEN = '{tokens.get('access_token')}'")
    print(f"REFRESH_TOKEN = '{tokens.get('refresh_token')}'")
    # print("Token Type:", tokens.get('token_type'))
    # print("Expires In:", tokens.get('expires_in'))
else:
    print("Error:", response.status_code)
    print(response.text)

