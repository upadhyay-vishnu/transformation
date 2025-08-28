import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows


class LoanWithdrawlReport(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path)
        df = drop_ending_rows(df)
        header_row = df.columns
        df = df[~df.apply(lambda row: row.equals(header_row), axis=1)]

        if "CASH" in df.columns:
            df["CASH"] = pd.to_numeric(df["CASH"], errors="coerce").fillna(0)
        df.columns = df.columns.str.strip()
        if "TRADE DATE" in df.columns:
            df['TRADE DATE'] = pd.to_datetime(df['TRADE DATE'], errors='coerce').dt.strftime("%Y-%m-%d")
        
        if "CHECK DATE" in df.columns:
            df['CHECK DATE'] = pd.to_datetime(df['CHECK DATE'], errors='coerce').dt.strftime("%Y-%m-%d")
    
        df.to_excel(self.output_path, index=False)
