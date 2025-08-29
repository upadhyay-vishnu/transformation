import pandas as pd

from .base import BaseTransformer
from .utils import drop_ending_rows

class AuditParticipantLevelActivityReport(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path, skiprows=3)
        df = drop_ending_rows(df)
        df.columns = df.columns.str.strip()
        if "Calendar Day" in df.columns:
            df['Calendar Day'] = pd.to_datetime(df['Calendar Day'], errors='coerce').dt.strftime("%m-%d-%Y")
        if "Process Date" in df.columns:
            df['Process Date'] = pd.to_datetime(df['Process Date'], errors='coerce').dt.strftime("%m-%d-%Y")
        df.to_excel(self.output_path, index=False)
