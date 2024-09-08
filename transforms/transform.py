import pandas as pd

class DataTransform:

    def __init__(self, file) -> None:
        self.df = pd.read_csv(file, sep=',', encoding='utf-8')
    
    def insert_id(self) -> None:
        self.df['id'] = range(1,len(self.df)+1)