import base64
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
# CLIENT_ID = "60b52514dac246419853e3abe3d297b4"
# CLIENTSECRET = "23672329e1944d949130ce4e6339c8aa"


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
            # release = []
            for album in albums:
                info = {
                    'album_name': album['name'],
                    'release_date': album['release_date'],
                    'total_tracks': album['total_tracks'],
                    'album_type': album['album_type'],
                    'artist_name': album['artists'][0]['name'],
                    'spotify_url': album['external_urls']['spotify'],
                    'album_image': album['images'][0]['url'] if album['images'] else None

                }
                # release.append(a)
                with open("output.json","a") as f:
                    json.dump(info, f, indent=2)
                    # print(output.json)
                # release = release.append[a]
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Error in latest release data fetching..", e)

get_new_release()