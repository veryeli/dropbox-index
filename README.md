This code creates an excel with an index of the properties of all of the folders and files in a dropbox and saves it as an excel

`pip install -r requirements.txt`

create a dropbox app

generate access token - allow access to whatever folder you want to use

get access token from app settings

Go to permissions and allow read access

copy `dropbox_config.example.py` to `dropbox_config.py`
enter the app token and get the other tokens with `python config.py`

`python scrape.py`
