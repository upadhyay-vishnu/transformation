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

        df.to_excel(self.output_path, index=False)
