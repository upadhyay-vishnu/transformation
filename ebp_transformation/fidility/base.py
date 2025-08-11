import abc

import pandas as pd


class BaseTransformer:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    @abc.abstractmethod
    def transform(self):
        pass


class NoTransformer(BaseTransformer):
    def transform(self):
        df = pd.read_excel(self.input_path)
        df.to_excel(self.output_path, index=False)
