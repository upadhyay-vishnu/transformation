import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows, get_header_row

class ParticipantContribution(BaseTransformer):
    def transform(self):

        expected_headers = [
            "Calendar Day",
            "DC Plan",
            "Source",
            "SSN - RESTRICTED",
            "Full Name - DC"
        ]
        header_row = get_header_row(self.input_path, expected_headers)
        
        if header_row is None:
            raise ValueError("Expected header not found in file")
        is_excel = False
        # Re-read Excel with correct header
        try:
            df =  pd.read_excel(self.input_path, header=header_row)
            is_excel = True
        except Exception:
            try:
                df =  pd.read_csv(self.input_path, header=header_row)
            except Exception as e:
                raise ValueError(f"Unsupported file format or corrupted file: {self.input_path}")
        df = drop_ending_rows(df)
        df.columns = df.columns.str.strip()
        if "Calendar Day" in df.columns:
            df['Calendar Day'] = pd.to_datetime(df['Calendar Day'], errors='coerce').dt.strftime("%m-%d-%Y")
        if "Process Date" in df.columns:
            df['Process Date'] = pd.to_datetime(df['Process Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        if  is_excel:
            df.to_excel(self.output_path, index=False)
        else:
            df.to_csv(self.output_path, index=False)
