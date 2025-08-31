import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows, get_header_row

class AuditRolloverReport(BaseTransformer):
    def transform(self):
        expected_headers = [
            "DC Plan Number",
            "Calendar Day",
            "SSN - RESTRICTED",
            "Full Name - DC"
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

        df = drop_ending_rows(df)
        if "Transaction" not in df.columns:
            raise ValueError("Missing required column: 'Transaction'")

        filtered_df = df[df["Transaction"].astype(str).str.strip().str.lower().str.contains("rollover in")]

        if "Calendar Day" in filtered_df.columns:
            filtered_df['Calendar Day'] = pd.to_datetime(filtered_df['Calendar Day'], errors='coerce').dt.strftime("%m-%d-%Y")
        if "Process Date" in filtered_df.columns:
            filtered_df['Process Date'] = pd.to_datetime(filtered_df['Process Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        filtered_df.to_excel(self.output_path, index=False)
