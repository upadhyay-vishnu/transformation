import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows


class BalanceInfoSummaryReportQ4(BaseTransformer):
    def transform(self):
        # Step 1: Read the input Excel file
        df = pd.read_excel(self.input_path, skiprows=5)
        print("===== Skipping first 5 Rows ======= \n")
        df = drop_ending_rows(df)
        df.to_excel(self.output_path, index=False)
