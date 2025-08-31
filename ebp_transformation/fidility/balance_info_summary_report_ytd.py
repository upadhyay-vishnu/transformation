import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows, get_header_row


class BalanceInfoSummaryReportYtd(BaseTransformer):
    def transform(self):
        # Step 1: Read the input Excel file
        expected_headers = [
            "DC Plan Number",
            "First Name - DC",
            "Last Name - DC"
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
        print("===== Skipping first 5 Rows ======= \n")
        df.columns = df.columns.str.strip()
        for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
            df[col] = df[col].dt.date
        df = drop_ending_rows(df)
        # Step 2: Define base and optional group-by columns
        base_group_cols = ["SSN", "First Name - DC", "Last Name - DC"]
        optional_cols = ["Hire Date", "Eligible Date", "Term Date", "Loan Repayment"]
        has_dob = "Date of Birth" in df.columns
        if has_dob:
            base_group_cols.append("Date of Birth")
        else:
            optional_cols.append("Date of Birth")
        # Step 3: Check for which optional columns are present in the file
        available_optional_cols = [col for col in optional_cols if col in df.columns]

        # Step 4: Group-by columns = base + available optional
        group_cols = base_group_cols + available_optional_cols

        # Step 5: Define numeric columns to sum (make sure they exist)
        sum_cols = ["Beginning Balance Cost $", "Contribution $", "Ending Balance Cost $"]
        existing_sum_cols = [col for col in sum_cols if col in df.columns]

        # Step 6: Perform groupby + aggregation
        grouped_df = df.groupby(group_cols, as_index=False)[existing_sum_cols].sum()

        # Step 7: Add missing optional columns (if any), set them to None
        missing_optional_cols = [col for col in optional_cols if col not in df.columns]
        for col in missing_optional_cols:
            grouped_df[col] = None

        # Step 8: Arrange final column order
        final_col_order = base_group_cols + available_optional_cols + existing_sum_cols + missing_optional_cols
        final_col_order = [col for col in final_col_order if col in grouped_df.columns]
        grouped_df = grouped_df[final_col_order]

        # Step 9: Save the transformed file
        if "Hire Date" in grouped_df.columns:
            grouped_df['Hire Date'] = pd.to_datetime(grouped_df['Hire Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        
        if "Term Date" in grouped_df.columns:
            grouped_df['Term Date'] = pd.to_datetime(grouped_df['Term Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        
        if "Date of Birth" in grouped_df.columns:
            grouped_df['Date of Birth'] = pd.to_datetime(grouped_df['Date of Birth'], errors='coerce').dt.strftime("%m-%d-%Y")
        
        if "Eligible Date" in grouped_df.columns:
            grouped_df['Eligible Date'] = pd.to_datetime(grouped_df['Eligible Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        
        if is_excel:
            grouped_df.to_excel(self.output_path, index=False)
        else:
            grouped_df.to_csv(self.output_path, index=False)
