import pandas as pd
from .utils import drop_ending_rows
from .base import BaseTransformer


class ContributionPlanLevelReport(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path, dtype=str, skiprows=1)
        # Drop completely empty rows
        df = drop_ending_rows(df)
        df.dropna(how="all", inplace=True)
        header = list(df.columns)

        df.reset_index(drop=True, inplace=True)
        df = df[~df.apply(lambda row: list(row) == header, axis=1)]
        df.columns = df.columns.str.strip()

        # Format Trade Date column to remove time component
        if "Trade Date" in df.columns:
            df['Trade Date'] = pd.to_datetime(df['Trade Date'], errors='coerce').dt.strftime("%Y-%m-%d")

        df.to_excel(self.output_path, index=False)
