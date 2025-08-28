import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows

class BalanceByFund(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path, skiprows=7)
        for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
            df[col] = df[col].dt.date
        df = drop_ending_rows(df)
        df.columns = df.columns.str.strip()
        # Replace blank or missing 'Fund ticker' values with '-'
        df["Fund Ticker Symbol"] = df["Fund Ticker Symbol"].fillna("-").replace("", "-", regex=False)

        if "As of Date" in df.columns:
            df['As of Date'] = pd.to_datetime(df['As of Date'], errors='coerce').dt.strftime("%Y-%m-%d")
        df.to_excel(self.output_path, index=False)
