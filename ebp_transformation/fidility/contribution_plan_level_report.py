import pandas as pd
from .utils import drop_ending_rows, get_header_row
from .base import BaseTransformer


class ContributionPlanLevelReport(BaseTransformer):
    def transform(self):
        epected_headers = [
            "Plan Number",
            "Partic SSN",
            "Trade Date"
        ]
        header_row = get_header_row(self.input_path, epected_headers)
        if header_row is None:
            raise ValueError("Expected header not found in file")
        try:
            df =  pd.read_excel(self.input_path, header=header_row)
        except Exception:
            try:
                df =  pd.read_csv(self.input_path, header=header_row)
            except Exception as e:
                raise ValueError(f"Unsupported file format or corrupted file: {self.input_path}")

        df = drop_ending_rows(df)
        df.dropna(how="all", inplace=True)
        header = list(df.columns)

        df.reset_index(drop=True, inplace=True)
        df = df[~df.apply(lambda row: list(row) == header, axis=1)]
        df.columns = df.columns.str.strip()

        if "Trade Date" in df.columns:
            df['Trade Date'] = pd.to_datetime(df['Trade Date'], errors='coerce').dt.strftime("%m-%d-%Y")

        df.to_excel(self.output_path, index=False)
