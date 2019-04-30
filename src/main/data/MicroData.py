import pandas as pd


class MicroData:

    def __init__(self, path: str):
        fmt = path.split(".")[1]
        if fmt == "csv":
            self.handler = CSVMicroData(path)
        else:
            self.handler = XLSXMicroData(path)

    def variants(self, item_code: int):
        self.handler.variants(item_code)

class CSVMicroData:

    def __init__(self, path: str):
        self.df = pd.read_csv(path, sep=";")

    def variants(self, item_code: int):
        maximum = 4
        aux = self.df.loc[self.df["CO_ITEM"] == item_code]
        results = []
        for i in range(maximum):
            results.append((aux.iloc[i, "TX_COR"], aux.iloc[i, "CO_POSICAO"]))
        return results

class XLSXMicroData:

    def __init__(self, path: str):
        self.df = pd.read_excel(path)

    def variants(self, item_code: int):
