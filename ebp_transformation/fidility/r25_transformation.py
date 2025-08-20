import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows

class AuditR25CheckRegister(BaseTransformer):
    def transform(self):
        """
        Reads the Excel file, filters rows where 'Check Deduction Type' is 'Federal Tax'
        or blank, then removes duplicates based on concatenated key
        from SSN, Full Name, Check Cleared Date, and Check Number.
        """

        df = pd.read_excel(self.input_path, skiprows=8)
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

        # Save to output
        df_final.to_excel(self.output_path, index=False)
