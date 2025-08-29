import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows

class AnnualLoanBalanceByPlan(BaseTransformer):
    def transform(self):
        """
        Groups loan data by SSN, Full name, Loan ID, and Origination date,
        then consolidates 'Outstanding Loan Balance Beginning' and
        'Outstanding Loan Balance Ending' values within each group.

        Args:
            csv_data (str): A string containing the input data in CSV format.

        Returns:
            pd.DataFrame: A DataFrame with consolidated loan entries.
        """
        df = pd.read_excel(self.input_path, skiprows=2)
        df = drop_ending_rows(df)
        df.columns = df.columns.str.strip()

        # Columns you want to group by
        grouping_columns = ["SSN - RESTRICTED", "Full Name - DC", "Loan ID", "Origination Date"]

        # 1. Clean whitespace/newlines from ALL grouping columns
        for col in grouping_columns:
            df[col] = (
                df[col]
                .astype(str)  # Convert to string
                .str.replace(r"[\r\n]+", " ", regex=True)  # Remove line breaks
                .str.strip()  # Remove surrounding spaces
            )

        # 2. Convert Origination Date to datetime
        df["Origination Date"] = pd.to_datetime(df["Origination Date"], errors="coerce").dt.normalize()

        # 3. Now get your Outstanding Loan Balance columns
        aggregation_columns = [col for col in df.columns if "Outstanding Loan Balance" in col]

        # 4. Prepare aggregation dictionary
        other_columns = [col for col in df.columns if col not in grouping_columns + aggregation_columns]
        agg_dict = {col: "first" for col in aggregation_columns + other_columns}

        # 5. Group
        consolidated_df = df.groupby(grouping_columns, as_index=False).agg(agg_dict)
        if "Origination Date" in consolidated_df.columns:
            consolidated_df['Origination Date'] = pd.to_datetime(consolidated_df['Origination Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        if "First Scheduled Payment Date" in consolidated_df.columns:
            consolidated_df['First Scheduled Payment Date'] = pd.to_datetime(consolidated_df['First Scheduled Payment Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        if "Final Payment Date" in consolidated_df.columns:
            consolidated_df['Final Payment Date'] = pd.to_datetime(consolidated_df['Final Payment Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        
        consolidated_df.to_excel(self.output_path, index=False)
