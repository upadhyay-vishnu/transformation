import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows

class BalanceByFund(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path, skiprows=7)
        df = drop_ending_rows(df)
        # Replace blank or missing 'Fund ticker' values with '-'
        df["Fund Ticker Symbol"] = df["Fund Ticker Symbol"].fillna("-").replace("", "-", regex=False)
        df.to_excel(self.output_path, index=False)
