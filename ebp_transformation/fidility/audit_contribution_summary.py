import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows

class ParticipantContributionPivotReport(BaseTransformer):
    def transform(self):
        # Step 1: Read input file
        df = pd.read_excel(self.input_path, skiprows=7)
        df = drop_ending_rows(df)
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
            "SAFE HARBOR MATCH",
            "EMPLOYEE DEFERRAL",
            "ROTH DEFERRAL",
            "EMPLOYER MATCH",
            "ROLLOVER",
            "ROTH ROLLOVER",
            "AFTER-TAX ROLLVER",
        ]
        for source in required_sources:
            if source not in pivot_df.columns:
                pivot_df[source] = 0

        # Step 6: Optional – Reorder columns
        ordered_cols = ["SSN", "Full Name"] + required_sources
        remaining_cols = [col for col in pivot_df.columns if col not in ordered_cols]
        final_cols = ordered_cols + remaining_cols

        pivot_df = pivot_df[final_cols]

        # Step 7: Save the output
        pivot_df.to_excel(self.output_path, index=False)
