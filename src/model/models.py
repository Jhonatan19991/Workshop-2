from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship

BASE = declarative_base()
MAX_STRING_SIZE = 100

class TheGrammyAwards(BASE):
    __tablename__ = 'TheGrammyAwards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    title = Column(String(MAX_STRING_SIZE), nullable=False)
    published_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    category = Column(String(MAX_STRING_SIZE), nullable=False)
    nominee = Column(String(MAX_STRING_SIZE), nullable=False)
    artist = Column(String(MAX_STRING_SIZE), nullable=False)
    workers = Column(String(MAX_STRING_SIZE), nullable=False)
    img = Column(String(MAX_STRING_SIZE), nullable=False)
    winner = Column(Boolean, nullable=False)
    
    def __str__ (self):
        return f" Table: {self.TheGrammyAwards.__table__}"