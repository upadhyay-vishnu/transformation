import pandas as pd

from .base import BaseTransformer


class AuditRolloverReport(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path)

        if "Transaction" not in df.columns:
            raise ValueError("Missing required column: 'Transaction'")

        filtered_df = df[df["Transaction"].astype(str).str.strip().str.lower().str.contains("rollover in")]

        filtered_df.to_excel(self.output_path, index=False)
