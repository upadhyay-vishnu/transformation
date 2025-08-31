import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows, get_header_row

class BalanceByFund(BaseTransformer):
    
    def transform(self):
        expected_headers = [
            "Calendar Day",
            "DC Plan",
            "Fund",
            "Fund Ticker Symbol",
            "Market Value",
            "Include all Participant Records"
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
        df = drop_ending_rows(df)
        df.columns = df.columns.str.strip()
        # Replace blank or missing 'Fund ticker' values with '-'
        df["Fund Ticker Symbol"] = df["Fund Ticker Symbol"].fillna("-").replace("", "-", regex=False)

        if "As of Date" in df.columns:
            df['As of Date'] = pd.to_datetime(df['As of Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        df.to_excel(self.output_path, index=False)
