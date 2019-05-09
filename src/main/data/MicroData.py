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
        sep = ";"
        if year == 2012:
            sep = ","
        self.df = pd.read_csv(path, sep=sep)
        self.separator_regex = re.compile("[_ ]")
        self.columns = list(self.df.columns.values)
        for c in range(len(self.columns)):
            n = self.columns[c].lower()
            if "cor" in n:
                self.color_col = c
            elif "item" in n:
                self.item_col = c
            elif "posicao" in n:
                self.position_col = c
            elif "area" in n:
                self.area_col = c
            elif "gabarito" in n:
                self.answer_col = c

    def variants(self, item_code: str)-> [Tuple[str, int]]:
        maximum = 4
        aux = self.df.loc[self.df[self.columns[self.item_col]] == int(item_code)]
        results = []
        for i in range(maximum):
            number = aux.iloc[i, self.position_col]
            if isinstance(number, str) and ("i" in number or "e" in number):
                number = number[:-1]
            results.append((aux.iloc[i, self.color_col],
                           numas(self.year,
                                 aux.iloc[i, self.area_col],
                                 int(number)
                                 )))
        return results

    def info(self, occurrence_idx: int, day: int, variant: str):
        num = occurrence_idx + 1
        domain = question_area(self.year, day, num)

        idx = occurrence_idx % get_mod(self.year, day)

        prep_var = variant.lower()[:-1]
        aux = self.df[self.df.apply(lambda x: prep_var in x[self.columns[self.color_col]].lower(), axis=1)]
        aux = aux[aux.apply(lambda x: domain in x[self.columns[self.area_col]], axis=1)]
        aux = aux.reset_index(drop=True)
        ref = aux.iloc[idx, self.item_col]
        ans = aux.iloc[idx, self.answer_col]
        ans = ord(ans[0]) - ord('A')
        return ref, ans

    def list_data(self, day: int, variant: str):
        prep_var = variant.lower()[:-1]
        aux = self.df[self.df.apply(lambda x: prep_var in x[self.columns[self.color_col]].lower(), axis=1)]
        mod = get_mod(self.year, day)
        areas = get_areas(self.year, day)

        item_codes = []
        answers = []
        for i in range(get_amount_questions(self.year, day)):
            idx = i % mod
            curr = aux[aux.apply(lambda x: areas[i] in x[self.columns[self.area_col]], axis=1)]
            curr = curr.reset_index(drop=True)
            item_codes.append(curr.iloc[idx, self.item_col])
            answers.append(ord(curr.iloc[idx, self.answer_col][0]) - ord('A'))
        return item_codes, answers

class XLSXMicroData:

    def __init__(self, path: str, year: int):
        self.year = year
        self.path = path
        self.areas = ["CHT", "CNT", "LCT", "MTT"]
        self.colors = ["azul", "amarelo", "branco", "rosa", "cinza"]
        self.df = {}
        for area in self.areas:
            self.df[area] = pd.read_excel(path, sheet_name=area)
        self.separator_regex = re.compile("[_ .]")

    def variants(self, item_code: str)-> [Tuple[str, int]]:
        maximum = 4
        results = []
        item_code = int(item_code)
        for area in self.areas:
            df = self.df[area]
            offset = self.get_offset(df, "azul")
            column_names = list(df.columns.values)
            aux = df.loc[df[column_names[offset + 1]] == item_code]
            count = aux.shape[0]

            if count > 0:
                for color in self.colors:
                    offset = self.get_item_code_col(df, color)
                    if offset == -1:
                        continue
                    aux = df.loc[df[column_names[offset]] == item_code]
                    number = aux.iloc[0, self.get_first_order(aux)]
                    if isinstance(number, str) and ("i" in number or "e" in number):
                        number = number[:-1]
                    m = int(number)

                    results.append((color, int(number)))
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

    def get_item_code_col(self, df: pd.DataFrame, name: str):
        column_names = list(df.columns.values)
        for c in range(len(column_names)):
            n = column_names[c].lower()
            if "cod" in n and name[:-1].lower() in n:
                return c
        return -1

    def get_first_order(self, df: pd.DataFrame):
        column_names = list(df.columns.values)
        for c in range(len(column_names)):
            n = column_names[c].lower()
            if "ordem" in n:
                return c
        return -1

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
        return -1

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

def numas(year: int, domain: str, num: int):
    if year >= 2017:
        if "LC".lower() in domain.lower():
            return num
        elif "CH".lower() in domain.lower():
            return num + 45
        elif "CN".lower() in domain.lower():
            return num + 90
        else:
            return num + 135
    else:
        if "CH".lower() in domain.lower():
            return num
        elif "CN".lower() in domain.lower():
            return num + 45
        elif "LC".lower() in domain.lower():
            return num + 90
        else:
            return num + 135
