import pandas as pd

from .base import BaseTransformer


class LoanWithdrawlReport(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path)
        header_row = df.columns
        df = df[~df.apply(lambda row: row.equals(header_row), axis=1)]

        if "CASH" in df.columns:
            df["CASH"] = pd.to_numeric(df["CASH"], errors="coerce").fillna(0)

        df.to_excel(self.output_path, index=False)
