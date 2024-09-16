from sqlalchemy import Column, Integer, String, DateTime, Boolean, TEXT
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