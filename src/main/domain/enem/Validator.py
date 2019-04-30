import io

import base64

import pandas as pd
from PIL import Image

from src.main.data.MicroData import MicroData
from src.main.domain.enem.PosProcessor import NATURAIS, HUMANAS, MATEMATICA, LINGUAGENS, INGLES, ESPANHOL


class ENEMValidator:

    def __init__(self,
                 year: int,
                 day: int,
                 variant: str,
                 micro: MicroData
                 ):
        self.year = year
        self.day = day
        self.variant = variant
        self.micro = micro

    def validate(self, questions):
        adt = (self.day - 1) * 90
        numbers = list(range(1 + adt, 46 + adt))
        amount_questions = 90
        if (self.year < 2017 and self.day == 2) or (self.year >= 2017 and self.day == 1):
            numbers = list(range(1 + adt, 6 + adt)) + list(range(1 + adt, 6 + adt)) + list(range(6 + adt, 46 + adt))
            amount_questions = 95
        numbers += list(range(46 + adt, 91 + adt))

        if self.year < 2017:
            if self.day == 1:
                domains = [HUMANAS] * 45 + [NATURAIS] * 45
            else:
                domains = [INGLES] * 5 + [ESPANHOL] * 5 + [LINGUAGENS] * 40 + [MATEMATICA] * 45
        else:
            if self.day == 1:
                domains = [INGLES] * 5 + [ESPANHOL] * 5 + [LINGUAGENS] * 40 + [HUMANAS] * 45
            else:
                domains = [NATURAIS] * 45 + [MATEMATICA] * 45

        item_codes, answers = self.micro.list_data(self.day, self.variant)

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
                print("answer is incorrect")
                print("Expected: " + str(answers[i]))
                print("Actual: " + str(questions[i]["answer"]))
                print("Question:")
                print(questions[i])
                return False

            view = str(questions[i]["view"])
            img_size = self.img_size(view)
            if img_size > 1000000:
                print("Img size is too high")
                print("Expected < 1000000")
                print("Actual: " + str(img_size))
                print("Question:")
                print(questions[i])
                return False

        for question in questions:
            view = str(question["view"])
            data_img = base64.b64decode(view)
            img = Image.open(io.BytesIO(data_img))
            img.show()

        return True

    def img_size(self, b64string):
        return (len(b64string) * 3) / 4 - b64string.count('=', -2)
