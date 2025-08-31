import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows, get_header_row

class AuditR25CheckRegister(BaseTransformer):
    def transform(self):
        """
        Reads the Excel file, filters rows where 'Check Deduction Type' is 'Federal Tax'
        or blank, then removes duplicates based on concatenated key
        from SSN, Full Name, Check Cleared Date, and Check Number.
        """

        expected_headers = [
            "Plan Number",
            "Plan Name",
            "SSN - RESTRICTED",
            "Employee Number",
            "Full Name"
        ]
        header_row = get_header_row(self.input_path, expected_headers)
        
        if header_row is None:
            raise ValueError("Expected header not found in file")
        is_excel = False
        try:
            df =  pd.read_excel(self.input_path, header=header_row)
            is_excel = True
        except Exception:
            try:
                df =  pd.read_csv(self.input_path, header=header_row)
            except Exception as e:
                raise ValueError(f"Unsupported file format or corrupted file: {self.input_path}")
    
        for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
            df[col] = df[col].dt.date
        df = drop_ending_rows(df)
        df.columns = df.columns.str.strip()

        # Filter where Check Deduction Type is 'Federal Tax' or blank (case-insensitive)
        df_filtered = df[
            df["Check Deduction Type"].isna()
            | (df["Check Deduction Type"].astype(str).str.strip().str.casefold() == "federal tax")
        ]

        # Create a concatenated key
        df_filtered["concat_key"] = (
            df_filtered["SSN - RESTRICTED"].astype(str).str.strip()
            + "_"
            + df_filtered["Full Name"].astype(str).str.strip()
            + "_"
            + df_filtered["Check Cleared Date"].astype(str).str.strip()
            + "_"
            + df_filtered["Check Number"].astype(str).str.strip()
        )
        df_final = df_filtered.drop_duplicates(subset=["concat_key"]).drop(columns=["concat_key"])

        if "Check Date" in df.columns:
            df['Check Date'] = pd.to_datetime(df['Check Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        if "Check Cleared Date" in df.columns:
            df['Check Cleared Date'] = pd.to_datetime(df['Check Cleared Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        # Save to output
        if is_excel:
            df_final.to_excel(self.output_path, index=False)
        else:
            df_final.to_csv(self.output_path, index=False)

