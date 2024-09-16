import pandas as pd
import sys
import os
import requests
import time
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
work_dir = os.getenv('WORK_DIR')


sys.path.append(work_dir)

class DataTransformGrammys:

    def __init__(self, file) -> None:
        self.df = pd.read_csv(file, sep=',', encoding='utf-8')
    
    def insert_id(self) -> None:
        self.df['id'] = range(1,len(self.df)+1)
    
    def set_winners(self) -> None:
        self.df['winner'] = self.df.groupby(['year', 'category']).cumcount() == 0
    
    def extract_artist(workers):
        if workers is None:
            return None
        
        match = re.search(r'\((.*?)\)', workers)
        if match:
            return match.group(1)
        return ""
    
    def set_artist_song_of_the_year(self) -> None:
        self.df.loc[self.df['category'] == 'Song Of The Year', 'artist'] = self.df['workers'].apply(self.extract_artist)

    
    def img(artist, csv_file='../data/img.csv'):
        if artist == None:
            return None

        if os.path.exists(csv_file):
            img_df = pd.read_csv(csv_file)

            if artist in img_df['artist'].values:
                return img_df[img_df['artist'] == artist]['image_url'].values[0]

        artist = artist.replace(' ','%20')
        resp = requests.get(f'https://www.last.fm/music/{artist}')
        try:
            time.sleep(1)
            soup = BeautifulSoup(resp.content, 'html.parser')
            car = soup.find(class_ = "section-with-separator buffer-standard visible-xs")
            rows = car.find(class_= 'image-list-item')
            img = rows.img['src']

            new_data = pd.DataFrame({'artist':[artist.replace('%20',' ')],'image_url':[img]})
            if os.path.exists(csv_file):
                new_data.to_csv(csv_file, mode='a', header=False, index=False)
            else:
                new_data.to_csv(csv_file, index=False)
        
            return img
        except:
            new_data = pd.DataFrame({'artist':[artist.replace('%20',' ')],'image_url':[None]})
            if os.path.exists(csv_file):
                new_data.to_csv(csv_file, mode='a', header=False, index=False)
            else:
                new_data.to_csv(csv_file, index=False)
            return None
    
    def set_img(self)->None:
        self.df['img'] = self.df['artist'].apply(lambda x: self.img(x))
    
    def various_artist(self) ->None:
        self.df['artist'] = self.df['artist'].str.replace(' featuring ', ';', regex=False)
        self.df['artist'] = self.df['artist'].str.replace(', ', ';', regex=False)

class DataTransformSpotify:

    def __init__(self, file) -> None:
        self.df = pd.read_csv(file, sep=',', encoding='utf-8')
    
    def drop_na(self) -> None:
        self.df.dropna()
    
    def drop_duplicates(self) -> None:
        self.df.drop_duplicates(subset='track_id', inplace=True)

        df_max_popularity_per_album = df.loc[df.groupby(['track_name', 'artists'])['popularity'].idxmax()]
        df = df_max_popularity_per_album.loc[df_max_popularity_per_album.groupby(['track_name', 'artists'])['popularity'].idxmax()]

    def map_genre(genre):
        genre_map = {
            'Rock': ['ska','alt-rock', 'hard-rock', 'punk-rock', 'psych-rock', 'rock', 'rock-n-roll', 'grunge', 'goth', 'rockabilly', 'guitar','garage','j-rock'],
            'Pop': ['pop', 'indie-pop', 'synth-pop', 'j-pop', 'k-pop', 'cantopop', 'mandopop', 'power-pop', 'pop-film'],
            'Electronic/Dance': ['hardstyle','disco','edm', 'house', 'techno', 'trance', 'dubstep', 'electro', 'chicago-house', 'deep-house', 'detroit-techno', 'progressive-house', 'club', 'dance', 'dancehall', 'drum-and-bass', 'idm', 'breakbeat', 'electronic','minimal-techno'],
            'Hip-Hop/Rap': ['hip-hop','trip-hop'],
            'Metal': ['metal', 'black-metal', 'death-metal', 'heavy-metal', 'metalcore', 'hardcore', 'grindcore'],
            'Jazz/Blues': ['jazz', 'blues', 'bluegrass','groove'],
            'Classical/Opera': ['classical', 'opera', 'piano','happy','romance','sad', 'comedy'],
            'Country/Folk': ['country', 'folk', 'honky-tonk'],
            'World Music': ['afrobeat', 'indian', 'iranian', 'j-dance', 'j-idol','brazil', 'french', 'german', 'malay', 'swedish', 'turkish', 'world-music','spanish','british'],
            'Latin': ['salsa', 'samba', 'pagode', 'mpb', 'forro', 'sertanejo', 'tango', 'latin', 'latino'],
            'Reggae': ['reggae', 'reggaeton', 'dub'],
            'Soundtrack/Film': ['anime', 'disney', 'show-tunes'],
            "Children's Music": ['children', 'kids'],
            'Ambient/New Age': ['ambient', 'chill', 'new-age', 'sleep', 'study'],
            'Punk': ['punk', 'emo'],
            'Soul/R&B': ['soul', 'r-n-b', 'funk', 'gospel'],
            'Alternative/Indie': ['alternative', 'indie','acoustic'],
            'Other': [ 'industrial', 'party','singer-songwriter']
        }
        for key, values in genre_map.items():
            if genre in values:
                return key
        return 'Other'

    def map_genre_df(self):
        self.df['track_genre'] = self.df['track_genre'].apply(self.map_genre)