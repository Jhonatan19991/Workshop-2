# http_operations.py
import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

def fetch_artist_image(artist, csv_file='./data/img.csv'):
    if artist is None:
        return None

    # Check if the image already exists in the CSV file
    if os.path.exists(csv_file):
        img_df = pd.read_csv(csv_file)
        if artist in img_df['artist'].values:
            return img_df[img_df['artist'] == artist]['image_url'].values[0]

    # Perform the HTTP request
    artist_escaped = artist.replace(' ', '%20')
    url = f'https://www.last.fm/music/{artist_escaped}'
    try:
        time.sleep(1)  # Be nice to the server
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        car = soup.find(class_="section-with-separator buffer-standard visible-xs")
        rows = car.find(class_='image-list-item')
        img_url = rows.img['src']

        # Save the image URL to the CSV file
        new_data = pd.DataFrame({'artist': [artist], 'image_url': [img_url]})
        if os.path.exists(csv_file):
            new_data.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            new_data.to_csv(csv_file, index=False)
        
        return img_url
    except Exception as e:
        # Save None in case of failure
        new_data = pd.DataFrame({'artist': [artist], 'image_url': [None]})
        if os.path.exists(csv_file):
            new_data.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            new_data.to_csv(csv_file, index=False)
        return None
