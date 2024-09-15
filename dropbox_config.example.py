ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN' # retreived from the dropbox app console
NAMESPACE_ID = 'YOUR_NAMESPACE_ID' # find the right one from print_namespaces()
ACCOUNT_ID =  'YOUR_ACCOUNT_ID' # be sure to get the TEAM MEMBER ID not the regular account id from print_members

APP_KEY = 'YOUR_APP_KEY' # From dropbox app console
APP_SECRET = 'YOUR_APP_SECRET' # From dropbox app console
AUTHORIZATION_CODE = 'YOUR_AUTHORIZATION_CODE' # From https://www.dropbox.com/oauth2/authorize?client_id=YOUR_APP_KEY&response_type=code&token_access_type=offline
REFRESH_TOKEN = 'YOUR_REFRESH_TOKEN' # From running code below :(
# TODO: Automate the refresh token process and selecting a namespace and account id
# this should all be do-able with only the app key and secret and other variables should be able
# to be saved in a generated file

# REFRESH_TOKEN = # https://stackoverflow.com/questions/71524238/how-to-create-not-expires-token-in-dropbox-api-v2


# from dropbox_config import APP_KEY, APP_SECRET, AUTHORIZATION_CODE

# import requests
# import base64



# # Encode your app key and secret for the Authorization header
# credentials = f"{APP_KEY}:{APP_SECRET}"
# base64_credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')

# # Set up the headers
# headers = {
#     'Authorization': f'Basic {base64_credentials}',
#     'Content-Type': 'application/x-www-form-urlencoded'
# }

# # Set up the form data
# data = {
#     'code': AUTHORIZATION_CODE,
#     'grant_type': 'authorization_code'
# }

# # Make the POST request to exchange the authorization code for tokens
# response = requests.post('https://api.dropbox.com/oauth2/token', headers=headers, data=data)

# # Process the response
# if response.status_code == 200:
#     tokens = response.json()
#     print("Access Token:", tokens.get('access_token'))
#     print("Refresh Token:", tokens.get('refresh_token'))
#     print("Token Type:", tokens.get('token_type'))
#     print("Expires In:", tokens.get('expires_in'))
# else:
#     print("Error:", response.status_code)
#     print(response.text)

