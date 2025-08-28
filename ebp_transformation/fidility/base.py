import abc

import pandas as pd
from .utils import drop_ending_rows

class BaseTransformer:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    @abc.abstractmethod
    def transform(self, skiprows: int = None):
        pass


class NoTransformer(BaseTransformer):
    def transform(self, skip_rows: int=None):
        df = pd.read_excel(self.input_path, skiprows=skip_rows)
        for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
            df[col] = df[col].dt.date
        df = drop_ending_rows(df)
        df.to_excel(self.output_path, index=False)
