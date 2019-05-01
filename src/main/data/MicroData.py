from typing import Dict, Tuple

import pandas as pd
import re

class MicroData:

    def __init__(self, path: str, year: int):
        fmt = path.split(".")[1]
        self.year = year
        if fmt == "csv":
            self.handler = CSVMicroData(path, year)
        else:
            self.handler = XLSXMicroData(path, year)

    def variants(self, item_code: str)-> [Tuple[str, int]]:
        return self.handler.variants(item_code)

    def info(self, occurrence_idx: int, day: int, variant: str):
        return self.handler.info(occurrence_idx, day, variant)

    def list_data(self, day: int, variant: str):
        return self.handler.list_data(day, variant)

class ENEMInfo:

    def __init__(self):
        self.micro_data: Dict[int, MicroData] = {}

    def add(self, year: int, path: str):
        self.micro_data[year] = MicroData(path, year)

    def available_years(self)-> [int]:
        return [int(k) for k in list(self.micro_data.keys())]

    def variants(self, year: int, item_code: str)-> [Tuple[str, int]]:
        if self.contains(year):
            return self.micro_data[year].variants(item_code)
        return []

    def contains(self, year: int):
        return year in self.micro_data

class CSVMicroData:

    def __init__(self, path: str, year: int):
        self.year = year
        self.df = pd.read_csv(path, sep=";")

    def variants(self, item_code: str)-> [Tuple[str, int]]:
        maximum = 4
        aux = self.df.loc[self.df["CO_ITEM"] == item_code]
        results = []
        for i in range(maximum):
            results.append((aux.iloc[i, "TX_COR"], aux.iloc[i, "CO_POSICAO"]))
        return results

    def info(self, occurrence_idx: int, day: int, variant: str):
        num = occurrence_idx + 1
        domain = question_area(self.year, day, num)

        idx = occurrence_idx % get_mod(self.year, day)

        aux = self.df.loc[self.df['TX_COR'] == variant]
        aux = aux.loc[domain in aux['SG_AREA']]
        ref = aux.iloc[idx, 2]
        ans = aux.iloc[idx, 3]
        ans = ord(ans[0]) - ord('A')
        return ref, ans

    def list_data(self, day: int, variant: str):
        aux = self.df.loc[self.df['TX_COR'] == variant]
        mod = get_mod(self.year, day)
        areas = get_areas(self.year, day)

        item_codes = []
        answers = []
        for i in range(get_amount_questions(self.year, day)):
            idx = i % mod
            aux = aux.loc[aux['SG_AREA'] == areas[i]]
            item_codes.append(aux.iloc[idx, 2])
            answers.append(ord(aux.iloc[idx, 3][0]) - ord('A'))
        return item_codes, answers

class XLSXMicroData:

    def __init__(self, path: str, year: int):
        self.year = year
        self.path = path
        self.areas = ["CHT", "CNT", "LCT", "MTT"]
        self.df = {}
        for area in self.areas:
            self.df[area] = pd.read_excel(path, sheet_name=area)
        self.separator_regex = re.compile("[_ ]")

    def variants(self, item_code: str)-> [Tuple[str, int]]:
        maximum = 4
        results = []
        item_code = int(item_code)
        for area in self.areas:
            df = self.df[area]
            column_names = list(df.columns.values)
            aux = df.loc[df[column_names[3]] == item_code]
            count = aux.shape[0]
            if count > 0:
                for i in range(maximum):
                    offset = 3 + (i * 4)
                    number = df.index[df[column_names[offset + 1]] == item_code].tolist()[0] + 1
                    variant = column_names[offset]
                    variant = self.separator_regex.split(variant)
                    variant = variant[1].upper()
                    results.append((variant, number))
                break
        return results

    def info(self, occurrence_idx: int, day: int, variant: str):
        num = occurrence_idx + 1
        domain = question_area(self.year, day, num) + "T"

        idx = occurrence_idx % get_mod(self.year, day)

        df = self.df[domain]
        variant = self.get_offset(df, variant)

        ref = df.iloc[idx, variant + 1]
        ans = ord(df.iloc[idx, variant + 2]) - ord('A')
        return ref, ans

    def get_offset(self, df: pd.DataFrame, name: str):
        maximum = 4
        column_names = list(df.columns.values)
        initial_columns_count = 0
        for c in range(len(column_names)):
            if "ordem" in column_names[c].lower():
                initial_columns_count = c
                break
        for i in range(maximum):
            offset = initial_columns_count + (i * 4)
            variant = column_names[offset]
            variant = self.separator_regex.split(variant)
            variant = variant[1].lower()
            if name[:-1].lower() in variant:
                return offset

    def list_data(self, day: int, variant: str):
        areas = ["CHT", "CNT"]
        amount = 90
        if day == 2:
            areas = ["LCT", "MTT"]
            amount = 95
        mod = get_mod(self.year, day)
        item_codes = []
        answers = []
        for area in areas:
            aux = self.df[area]
            offset = self.get_offset(aux, variant)
            for i in range(mod):
                if len(item_codes) == amount:
                    break
                item_codes.append(aux.iloc[i, offset + 1])
                answers.append(ord(aux.iloc[i, offset + 2]) - ord('A'))
        return item_codes, answers

def get_areas(year, day):
    if year < 2017:
        if day == 1:
            return ["CH"] * 45 + ["CN"] * 45
        else:
            return ["LC"] * 50 + ["MT"] * 45
    else:
        if day == 1:
            return ["LC"] * 50 + ["CH"] * 45
        else:
            return ["CN"] * 45 + ["MT"] * 45


def get_amount_questions(year, day):
    amount = 90
    if (year < 2017 and day == 2) or (year >= 2017 and day == 1):
        amount = 95
    return amount

def get_mod(year, day):
    mod = 45
    if (year < 2017 and day == 2) or (year >= 2017 and day == 1):
        mod = 50
    return mod

def question_area(year: int, day: int, num: int):
    domain = "LC"
    if year >= 2017:
        if day == 2:
            if num <= 45:
                domain = "CN"
            else:
                domain = "MT"
        elif num >= 51:
            domain = "CH"
    else:
        if day == 2:
            if num >= 51:
                domain = "MT"
        elif day == 1:
            if num <= 45:
                domain = "CH"
            else:
                domain = "CN"
    return domain
