import pandas as pd
import sys
import os
from dotenv import load_dotenv
from decouple import config

load_dotenv()
work_dir = os.getenv('WORK_DIR')


sys.path.append(work_dir)

from transforms.transform import *
from src.model.models import *
from src.database.dbconnection import getconnection
from sqlalchemy import inspect, Table, MetaData, insert, select
import json
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.exc import SQLAlchemyError
import logging as log
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload

import io

def extract_grammy(**kwargs):
    engine = getconnection()
    Session = sessionmaker(bind=engine)
    session = Session()
    log.info("Starting data extraction")
    table = aliased(TheGrammyAwards)
    query = str(session.query(table).statement)
    df = pd.read_sql(query, con=engine)
    log.info(f"Finish the data extraction {df}")
    kwargs['ti'].xcom_push(key='grammy_data', value=df.to_json(orient='records'))
    return df.to_json(orient='records')





def transform_grammy(**kwargs):
    log.info("Starting Data transform")
    ti = kwargs['ti']
    str_data = ti.xcom_pull(task_ids="read_db", key='grammy_data')
    if str_data is None:
        log.error("No data found in XCom for 'grammy_data'")
        return

    json_df = json.loads(str_data)
    df = pd.json_normalize(data=json_df)
    log.info(f"Data is {df}")
    file = DataTransformGrammys('./data/the_grammy_awards.csv')
    file.set_df(df)
    file.set_winners()
    file.set_artist_song_of_the_year()
    file.set_img()
    file.various_artist()

    df = file.df.copy()

    df_grouped = df.groupby(['nominee', 'artist','year', 'img']).agg(
        nominee_times=('nominee', 'size'),
        wins=('winner', 'sum')
    ).reset_index()

    df_grouped.columns = ['nominee', 'artist', 'year','img', 'nominee_times', 'wins']

    log.info('Aggregated DataFrame created')


    result = {
        "source": "grammy",
        "data": df_grouped.to_dict(orient='records')
    }
    kwargs['ti'].xcom_push(key='transformed_grammy_data', value=json.dumps(result))
    log.info('columns: ', df_grouped.columns)
    return json.dumps(result)


    

def read_spotify(**kwargs):
    log.info("Starting Spotify extraction")
    df = pd.read_csv('./data/spotify_dataset.csv')
    log.info('Spotify Dataset Read Successfully')
    kwargs['ti'].xcom_push(key='spotify_data', value=df.to_json(orient='records'))
    return df.to_json(orient='records')

def tranform_spotify(**kwargs):
    log.info("Starting Spotify transform")
    
    ti = kwargs["ti"]
    log.info("the kwargs are: ", kwargs)
    str_data = ti.xcom_pull(task_ids="read_csv", key='spotify_data')
    if str_data is None:
        log.error("No data found in XCom for 'spotify_data'")
        return

    json_df = json.loads(str_data)
    df = pd.json_normalize(data=json_df)
    log.info(f"Data is {df}")
    file = DataTransformSpotify(df)
    file.drop_na()
    file.drop_duplicates()
    file.map_genre_df()
    log.info('Successfully transformed')
    result = {
        "source": "spotify",
        "data": file.df.to_dict(orient='records')
    }
    kwargs['ti'].xcom_push(key='spotify_data', value=json.dumps(result))

    return json.dumps(result)

def merge_df(**kwargs):
    log.info("Starting data merge")

    ti = kwargs["ti"]
    
    # Pull data from XCom
    json_grammy = ti.xcom_pull(task_ids="transform_db", key='transformed_grammy_data')
    json_spotify = ti.xcom_pull(task_ids="transform_csv", key='spotify_data')

    log.info(json_grammy)
    # Check if the data exists
    if json_grammy is None:
        log.error("No data found in XCom for 'transform_grammy'")
        return

    if json_spotify is None:
        log.error("No data found in XCom for 'transform_csv'")
        return


    # Load data into DataFrames
    data_grammy = json.loads(json_grammy)
    data_spotify = json.loads(json_spotify)

    df_grammy = pd.DataFrame(data_grammy["data"])
    df_spotify = pd.DataFrame(data_spotify["data"])

    # Perform the merge
    df_spotify['track_name'] = df_spotify['track_name'].str.lower()
    df_grammy['nominee'] = df_grammy['nominee'].str.lower()

    df_merged = df_spotify.merge(df_grammy, how='left', left_on='track_name', right_on='nominee')

    df_merged['nominee_times'] = df_merged['nominee_times'].fillna(0).astype(int)
    df_merged['wins'] = df_merged['wins'].fillna(0).astype(int)

    dfs = df_merged.groupby('track_name')['popularity'].idxmax()

    max_popularities = df_merged.loc[dfs].set_index('track_name')['popularity']

    mask = df_merged['popularity'] < df_merged['track_name'].map(max_popularities)

    df_merged.loc[mask, ['nominee_times', 'wins', 'img']] = 0, 0, None
    
    log.info(f"Merged DataFrame shape: {df_merged.shape}")
    log.info(f"Merged DataFrame columns: {df_merged.columns}")

    return df_merged.to_json(orient='records')



def load_merge(**kwargs):
    log.info("Starting load merge")

    # Obtener datos del XCom
    ti = kwargs['ti']
    json_df = ti.xcom_pull(task_ids="merge")
    if json_df is None:
        log.error("No data found in XCom for 'merge'")
        return

    # Convertir JSON a DataFrame
    df = pd.DataFrame(json.loads(json_df))
    log.info(df)
    df.drop(columns=['artist','nominee'], inplace=True)
    # Conectar a la base de datos
    engine = getconnection()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear la tabla si no existe
    try:
        if inspect(engine).has_table('SongsStatitics'):
            SongsStatitics.__table__.drop(engine)
        SongsStatitics.__table__.create(engine)
        log.info("Table created successfully.")
    except SQLAlchemyError as e:
        log.error(f"Error creating table: {e}")
        return

    try:
        df.drop_duplicates(subset='id', inplace=True)
        log.info(df.shape)
        df.to_sql('SongsStatitics', con=engine, if_exists='append', index=False)
        log.info('Data loaded successfully')
        return df.to_json(orient='records')
    except Exception as e:
        log.error(f"Error loading data: {e}")


def store(**kwargs):
    log.info('starting data store')
    ti = kwargs['ti']
    json_df = ti.xcom_pull(task_ids="load")
    if json_df is None:
        log.error("No data found in XCom for 'load'")
        return

    df = pd.DataFrame(json.loads(json_df))


    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = './driveapi.json'   
    PARENT_FOLDER_ID = "1b5v12-Pv__zvUSYQYalEmJ5Dcy96rnMg"
    

    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    file_metadata = {
        'name': 'SpotifyData.csv',
        'parents': [PARENT_FOLDER_ID],
        'mimeType': 'text/csv'
    }

    # Convert CSV string to bytes
    csv_bytes = csv_buffer.getvalue().encode('utf-8')
    media = MediaInMemoryUpload(csv_bytes, mimetype='text/csv')

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

