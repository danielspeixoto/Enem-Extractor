import io

import base64
import pandas as pd
from PIL import Image

from src.main.domain.PosProcessor import NATURAIS, HUMANAS, MATEMATICA, LINGUAGENS, INGLES, ESPANHOL


class Validator:

    def __init__(self,
                 year: int,
                 day: int,
                 variant: str,
                 micro_data_path: str
                 ):
        self.year = year
        self.day = day
        self.variant = variant
        self.microdata_path = micro_data_path

    def validate(self, questions):
        adt = (self.day - 1) * 90
        numbers = list(range(1 + adt, 46 + adt))
        amount_questions = 90
        mod = 45
        if (self.year < 2017 and self.day == 2) or (self.year >= 2017 and self.day == 1):
            numbers = list(range(1 + adt, 6 + adt)) + list(range(1 + adt, 6 + adt)) + list(range(6 + adt, 46 + adt))
            amount_questions = 95
            mod = 50
        numbers += list(range(46 + adt, 91 + adt))

        if self.year < 2017:
            if self.day == 1:
                domains = [HUMANAS] * 45 + [NATURAIS] * 45
                areas = ["CH"] * 45 + ["CN"] * 45
                positions = list(range(1, 46)) + list(range(1, 46))
            else:
                domains = [INGLES] * 5 + [ESPANHOL] * 5 + [LINGUAGENS] * 40 + [MATEMATICA] * 45
                areas = ["LC"] * 50 + ["MT"] * 45
                positions = list(range(1, 51)) + list(range(1, 46))
        else:
            if self.day == 1:
                domains = [INGLES] * 5 + [ESPANHOL] * 5 + [LINGUAGENS] * 40 + [HUMANAS] * 45
                areas = ["LC"] * 50 + ["CH"] * 45
                positions = list(range(1, 51)) + list(range(1, 46))
            else:
                domains = [NATURAIS] * 45 + [MATEMATICA] * 45
                areas = ["CN"] * 45 + ["MT"] * 45
                positions = list(range(1, 46)) + list(range(1, 46))

        item_codes = []
        answers = []
        df = pd.read_csv(self.microdata_path, sep=";")
        df = df.loc[df['TX_COR'] == self.variant]
        for i in range(amount_questions):
            idx = i % mod
            aux = df.loc[df['SG_AREA'] == areas[i]]
            testId = aux.iloc[0, 6]
            if aux.iloc[idx, 0] != positions[i]:
                print("Incorrect validation, returning wrong item codes")
                print("Idx: " + str(i) + " Position: " + str(positions[i]))
                return False
            item_codes.append(aux.iloc[idx, 2])
            answers.append(ord(aux.iloc[idx, 3][0]) - ord('A'))

        for i in range(amount_questions):
            if str(questions[i]["number"]) != str(numbers[i]):
                print("number is incorrect")
                print("Expected: " + str(numbers[i]))
                print("Actual: " + str(questions[i]["number"]))
                print("Question:")
                print(questions[i])
                return False

            if str(questions[i]["stage"]) != str(self.day):
                print("stage is incorrect")
                print("Expected: " + str(self.day))
                print("Actual: " + str(questions[i]["stage"]))
                print("Question:")
                print(questions[i])
                return False

            if str(questions[i]["edition"]) != str(self.year):
                print("edition is incorrect")
                print("Expected: " + str(self.year))
                print("Actual: " + str(questions[i]["edition"]))
                print("Question:")
                print(questions[i])
                return False

            if str(questions[i]["domain"]) != str(domains[i]):
                print("domain is incorrect")
                print("Expected: " + str(domains[i]))
                print("Actual: " + str(questions[i]["domain"]))
                print("Question:")
                print(questions[i])
                return False

            if str(questions[i]["itemCode"]) != str(item_codes[i]):
                print("itemCode is incorrect")
                print("Expected: (" + str(item_codes[i]) + ")")
                print("Actual: (" + str(questions[i]["itemCode"]) + ")")
                print("Question:")
                print(questions[i])
                return False

            if str(questions[i]["answer"]) != str(answers[i]):
                print("domain is incorrect")
                print("Expected: " + str(answers[i]))
                print("Actual: " + str(questions[i]["domain"]))
                print("Question:")
                print(questions[i])
                return False

        # for q in questions:
        #     data_img = base64.b64decode(str(q["view"]))
        #     img = Image.open(io.BytesIO(data_img))
        #     img.show()

        return True
