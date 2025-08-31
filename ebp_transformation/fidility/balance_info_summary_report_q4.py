import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows, get_header_row


class BalanceInfoSummaryReportQ4(BaseTransformer):
    def transform(self):
        # Step 1: Read the input Excel file
        expected_headers = [
            "DC Plan Number",
            "First Name - DC",
            "Last Name - DC",
            "Division Name",
            "Division Code - DC",
            "Fund",
        ]
        header_row = get_header_row(self.input_path, expected_headers)
        
        if header_row is None:
            raise ValueError("Expected header not found in file")

        # Re-read Excel with correct header
        try:
            df =  pd.read_excel(self.input_path, header=header_row)
        except Exception:
            try:
                df =  pd.read_csv(self.input_path, header=header_row)
            except Exception as e:
                raise ValueError(f"Unsupported file format or corrupted file: {self.input_path}")
        for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
            df[col] = df[col].dt.date
        print("===== Skipping first 5 Rows ======= \n")
        df = drop_ending_rows(df)
        df.to_excel(self.output_path, index=False)
