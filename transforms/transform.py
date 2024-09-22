import pandas as pd
import sys
import os
import re
from dotenv import load_dotenv
from .http_operations import fetch_artist_image

load_dotenv()
work_dir = os.getenv('WORK_DIR')


sys.path.append(work_dir)

import re

def extract_artist(workers: str, artist: str) -> str:
    """Extracts the artist's name from the 'workers' string if 'artist' is not defined.
    If an artist is found in parentheses, that name is returned.
    """
    if not artist:
        if workers:
            match = re.search(r"\((.*?)\)", workers)  # Corrección de la expresión regular
            if match:
                return match.group(1)
        return None
    return artist


class DataTransformGrammys:

    def __init__(self, file) -> None:
        """Initializes the class by loading a CSV file into a DataFrame."""
        self.df = pd.read_csv(file, sep=',', encoding='utf-8')
    
    def set_df(self, df) ->None:
        """Sets a new DataFrame in the instance."""
        self.df = df
    
    def insert_id(self) -> None:
        """Adds an 'id' column to the DataFrame with a range of sequential numbers."""
        self.df['id'] = range(1,len(self.df)+1)

    def update_and_clear_artist(self):
        """Updates the 'workers' column for artists containing 'songwriter' and clears the 'artist' column."""
        mask = self.df['artist'].str.contains('songwriter', case=False, na=False)
        
        # Copiar el contenido de 'artist' a 'workers' y borrar 'artist'
        self.df.loc[mask, 'workers'] = self.df.loc[mask, 'artist']
        self.df.loc[mask, 'artist'] = None

        
    def set_winners(self) -> None:
        """Marks the winners in the DataFrame, assigning True to the first artist in each year and category group."""
        self.df['winner'] = self.df.groupby(['year', 'category']).cumcount() == 0
        
    def set_artist_song_of_the_year(self) -> None:
        """Updates the 'artist' column using the extract_artist function to handle 'workers' cases."""
        self.df['workers'] = self.df['workers'].astype(str)

        self.df['artist'] = self.df.apply(lambda row: extract_artist(row['workers'], row['artist']), axis=1)

    
    def set_img(self)->None:
        """Adds an 'img' column to the DataFrame, using an external function to fetch the artist's image."""
        self.df['img'] = self.df['artist'].apply(lambda x: fetch_artist_image(x))
    
    def various_artist(self) ->None:
        """Normalizes artist names with multiple collaborations by replacing separators with ';'."""
        self.df['artist'] = self.df['artist'].str.replace(' featuring ', ';', regex=False)
        self.df['artist'] = self.df['artist'].str.replace(' Featuring ', ';', regex=False)

        self.df['artist'] = self.df['artist'].str.replace(', ', ';', regex=False)
        self.df['artist'] = self.df['artist'].str.replace(' ,', ';', regex=False)
        self.df['artist'] = self.df['artist'].str.replace(' , ', ';', regex=False)

        self.df['artist'] = self.df['artist'].str.replace(' & ', ';', regex=False)
        self.df['artist'] = self.df['artist'].str.replace(' With ', ';', regex=False)

class DataTransformSpotify:

    def __init__(self, df) -> None:
        """Initializes the class with an existing DataFrame."""
        self.df = df
    
    def drop_na(self) -> None:
        """Removes all rows with null values from the DataFrame."""
        self.df.dropna()
    
    def drop_duplicates(self) -> None:
        """Removes duplicates in the DataFrame based on the 'track_id' column."""
        self.df.drop_duplicates(subset='track_id', inplace=True)

        df_max_popularity_per_album = self.df.loc[self.df.groupby(['track_name', 'artists'])['popularity'].idxmax()]
        self.df = df_max_popularity_per_album.loc[df_max_popularity_per_album.groupby(['track_name', 'artists'])['popularity'].idxmax()]

    @staticmethod
    def map_genre(genre):
        """Maps musical genres to broader categories for simplified analysis."""
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
        """Applies the map_genre function to the 'track_genre' column of the DataFrame to classify genres."""
        self.df['track_genre'] = self.df['track_genre'].apply(self.map_genre)
