import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows

class AuditRolloverReport(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path, skiprows=3)
        df = drop_ending_rows(df)
        if "Transaction" not in df.columns:
            raise ValueError("Missing required column: 'Transaction'")

        filtered_df = df[df["Transaction"].astype(str).str.strip().str.lower().str.contains("rollover in")]

        filtered_df.to_excel(self.output_path, index=False)
