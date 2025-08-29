import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows

class AuditInvestmentElectionsAsOfaSpecificDate(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path, skiprows=4)
        df = drop_ending_rows(df)
        df.columns = df.columns.str.strip()
        if "Hire Date" in df.columns:
            df['Hire Date'] = pd.to_datetime(df['Hire Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        if "Termination Date" in df.columns:
            df['Termination Date'] = pd.to_datetime(df['Termination Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        df.to_excel(self.output_path, index=False)