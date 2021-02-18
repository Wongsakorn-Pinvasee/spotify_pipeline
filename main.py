import configparser
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

# read config file
config = configparser.ConfigParser()
config.read('config.ini')

DATABASE_LOCATION = 'sqlite:///my_played_tracks.sqlite'
USER_ID = config['spotify']['user_id']
TOKEN = config['spotify']['token']

if __name__ == '__main__':

    # Extract
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer {token}'.format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    url = 'https://api.spotify.com/v1/me/player/recently-played?after={time}'.format(time=yesterday_unix_timestamp)
    r = requests.get(url, headers=headers)

    data = r.json()

    songs = []
    artists = []
    played_at = []
    timestamps = []


    for song in data['items']:
        songs.append(song['track']['name'])
        artists.append(song['track']['album']['artists'][0]['name'])
        played_at.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])
           
    song_dict = {
        'song' : songs,
        'artist': artists,
        'played_at' : played_at,
        'timestamp' : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ['song', 'artist', 'played_at', 'timestamp'])
    print(song_df.head())