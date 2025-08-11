import pandas as pd

from .base import BaseTransformer


class BalanceByFund(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path)

        # Replace blank or missing 'Fund ticker' values with '-'
        df["Fund Ticker Symbol"] = df["Fund Ticker Symbol"].fillna("-").replace("", "-", regex=False)
        df.to_excel(self.output_path, index=False)
