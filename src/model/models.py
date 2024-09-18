from sqlalchemy import Column, Integer, String, DateTime, Boolean, TEXT, Float
from sqlalchemy.orm import declarative_base, relationship

BASE = declarative_base()
MAX_STRING_SIZE = 256

class TheGrammyAwards(BASE):
    __tablename__ = 'TheGrammyAwards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    title = Column(String(MAX_STRING_SIZE), nullable=False)
    published_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    category = Column(String(MAX_STRING_SIZE), nullable=False)
    nominee = Column(String(MAX_STRING_SIZE), nullable=True)
    artist = Column(String(MAX_STRING_SIZE), nullable=True)
    workers = Column(TEXT, nullable=True)
    img = Column(TEXT, nullable=True)
    winner = Column(Boolean, nullable=False)
    
    def __str__ (self):
        return f" Table: {self.TheGrammyAwards.__table__}"

class SongsStatitics(BASE):

    
    __tablename__ = 'SongsStatitics'
    id = Column(Integer, primary_key=True, autoincrement=True)

    track_id = Column(String(MAX_STRING_SIZE), nullable=False)
    artists = Column(String, nullable=False)
    album_name = Column(String(MAX_STRING_SIZE), nullable=False)
    track_name = Column(String, nullable=False)
    popularity = Column(Integer, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    explicit = Column(Boolean, nullable=True)
    danceability = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    key = Column(Integer, nullable=True)
    loudness = Column(Float, nullable=False)
    mode = Column(Integer, nullable=False)
    speechiness = Column(Float, nullable=False)
    acousticness = Column(Float, nullable=False)
    instrumentalness = Column(Float, nullable=False)
    liveness = Column(Float, nullable=False)
    valence = Column(Float, nullable=False)
    tempo = Column(Float, nullable=True)
    time_signature = Column(Float, nullable=True)
    track_genre = Column(String, nullable=True)
    
    img = Column(TEXT, nullable=True)
    nominee_times = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)

    
    
    def __str__ (self):
        return f" Table: {self.SongsStatitics.__table__}"

