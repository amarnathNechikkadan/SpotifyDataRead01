import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def access_token():
    try:
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {encoded_credentials}"},
            data={"grant_type": "client_credentials"}
        )
        return response.json()["access_token"]
    except Exception as e:
        print("Error in token generation...", e)

def get_new_release():
    try:
        token = access_token()
        header = {'Authorization': f'Bearer {token}'}
        param = {'limit': 50 }  # smaller for testing
        response = requests.get("https://api.spotify.com/v1/browse/new-releases",
                                headers=header, params=param)
        if response.status_code == 200:
            data = response.json()
            albums = data['albums']['items']
            release = []
            for i in albums:
                a = {
                    'album_name': i['name'],
                    'release_date': i['release_date'],

                }
                # release.append(a)
                print(a)
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Error in latest release data fetching..", e)

get_new_release()