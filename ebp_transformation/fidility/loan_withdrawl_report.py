import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows, get_header_row


class LoanWithdrawlReport(BaseTransformer):
    def transform(self):
        expected_headers = [
            "PLAN",
            "SSN",
            "PARTICIPANT NAME"
        ]
        header_row = get_header_row(self.input_path, expected_headers)
        
        if header_row is None:
            raise ValueError("Expected header not found in file")

        # Re-read Excel with correct header
        is_excel = False
        try:
            df =  pd.read_excel(self.input_path, header=header_row)
            is_excel = True
        except Exception:
            try:
                df =  pd.read_csv(self.input_path, header=header_row)
            except Exception as e:
                raise ValueError(f"Unsupported file format or corrupted file: {self.input_path}")
        df = drop_ending_rows(df)
        header_row = df.columns
        df = df[~df.apply(lambda row: row.equals(header_row), axis=1)]

        # if "CASH" in df.columns:
        #     df["CASH"] = pd.to_numeric(df["CASH"], errors="coerce").fillna(0)
        df.columns = df.columns.str.strip()
        if "TRADE DATE" in df.columns:
            df['TRADE DATE'] = pd.to_datetime(df['TRADE DATE'], errors='coerce').dt.strftime("%m-%d-%Y")
        
        if "CHECK DATE" in df.columns:
            df['CHECK DATE'] = pd.to_datetime(df['CHECK DATE'], errors='coerce').dt.strftime("%m-%d-%Y")
        if is_excel:
            df.to_excel(self.output_path, index=False)
        else:
            df.to_csv(self.output_path, index=False)
            
