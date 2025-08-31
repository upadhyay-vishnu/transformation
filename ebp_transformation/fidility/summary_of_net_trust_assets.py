import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows, get_header_row

class SummaryOfNetTrustAssets(BaseTransformer):
    def transform(self):

        expected_headers = [
            "Fund Name",
            "Historical Cost",
            "Price",
            "Total Market Value"
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
        df.dropna(how="all", inplace=True)
        if "Price" in df.columns:
            price_col = "Price"
        else:
            price_col = df.columns[3]

        # Deleting rows after Net Asset
        net_asset_idx = df[df[price_col].astype(str).str.strip().str.casefold().eq("net asset")].index

        if not net_asset_idx.empty:
            cutoff_idx = net_asset_idx[0] + 1
            df = df.iloc[:cutoff_idx]

        net_asset_index = df.apply(lambda row: row.astype(str).str.contains("NET ASSETS")).any(axis=1)
        net_asset_row = df[net_asset_index].index[0]
        # Remove all rows after the Net Asset row
        df = df.loc[:net_asset_row]

        # Move 'Net Asset' label to Fund Name and shift value to Total Mark Value
        net_asset_row_data = df.loc[net_asset_row].copy()
        df.loc[net_asset_row, "Fund Name"] = net_asset_row_data["Price"]
        df.loc[net_asset_row, "Total Market Value"] = net_asset_row_data["Total Market Value"]
        df.loc[net_asset_row, ["Price", "Historic Cost", "Share Balance"]] = None
        df = df[df["Fund Name"].astype(str).str.strip() != ""]
        if is_excel:
            df.to_excel(self.output_path, index=False)
        else:
            df.to_csv(self.output_path, index=False)