import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows, get_header_row

class ParticipantContributionPivotReport(BaseTransformer):
    def transform(self):
        # Step 1: Read input file
        expected_headers = [
            "Calendar Day",
            "Plan Number",
            "Plan Name",
            "Source",
            "SSN"
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
        has_source = "Source" in df.columns
        if not has_source:
            df.to_excel(self.output_path, index=False)
            return
        df["Source"] = df["Source"].astype(str).str.replace(r"^\d+-\s*", "", regex=True).str.strip()
        required_cols = ["SSN", "Full Name", "Source", "Transaction Cash Amount"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Step 3: Pivot the table
        pivot_df = pd.pivot_table(
            df,
            index=["SSN", "Full Name"],
            columns="Source",
            values="Transaction Cash Amount",
            aggfunc="sum",
            fill_value=0,
        ).reset_index()

        pivot_df.columns.name = None  # remove 'Source' from columns
        pivot_df.columns = [str(col) for col in pivot_df.columns]

        # Step 5: Ensure all required source columns exist
        required_sources = [
            "EMPLOYEE DEFERRAL",
            "ROTH DEFERRAL",
            "EMPLOYER MATCH",
            "ROLLOVER",
            "ROTH ROLLOVER",
            "AFTER-TAX ROLLVER",
            "ER PROFIT SHARING"
        ]
        for source in required_sources:
            if source not in pivot_df.columns:
                pivot_df[source] = 0

        # Step 6: Optional – Reorder columns
        if "Status" not in pivot_df.columns:
            pivot_df["Status"] = ""
        ordered_cols = ["SSN", "Full Name", "Status"] + required_sources
        remaining_cols = [col for col in pivot_df.columns if col not in ordered_cols]
        final_cols = ordered_cols + remaining_cols

        pivot_df = pivot_df[final_cols]

        # Step 7: Save the output
        if is_excel:
            pivot_df.to_excel(self.output_path, index=False)
        else:
            pivot_df.to_csv(self.output_path, index=False)
