import os

import base64

from src.main.aggregates.pdf_item import Question
from src.main.data.MicroData import MicroData
from src.main.data.Vision import pdf2multiple_img

INGLES = "inglês"
ESPANHOL = "espanhol"
LINGUAGENS = "linguagens"
MATEMATICA = "matemática"
HUMANAS = "humanas"
NATURAIS = "naturais"

class ENEMPosProcessor:

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

    def pos_process(self,
                    pdf_input_path, question: Question, working_dir):
        question_folder = working_dir + "/question/"
        os.mkdir(question_folder, 0o755)

        output = working_dir + "/out.pdf"
        question.save_as_pdf(pdf_input_path, question_folder, output)

        output_img = working_dir + "/out.jpg"

        img_dir = working_dir + "/img/"
        os.mkdir(img_dir)
        pdf2multiple_img(img_dir, output, output_img)

        domain = self.area(question.occurrence_idx, self.day)
        question_num = self.number(question.occurrence_idx, self.day)
        ref, ans = self.micro.info(question.occurrence_idx, self.day, self.variant)

        tags = [domain.lower()]

        with open(output_img, "rb") as file:
            view = base64.b64encode(file.read()).decode()

        meta = {
            "edition": self.year,
            "stage": self.day,
            "source": "ENEM",
            "variant": self.variant,
            "domain": domain,
            "number": question_num,
            "answer": ans,
            "view": view,
            "itemCode": str(ref),
            "tags": tags,
            "referenceId": "ENEM-" + str(self.year) + "-" + str(self.day) + "-" + str(question.occurrence_idx)
        }

        return meta

    def area(self, occurrence_idx: int, day: int):
        num = occurrence_idx + 1
        if day == 2:
            num += 90
        if self.year < 2017:
            if day == 1:
                if num <= 45:
                    return HUMANAS
                else:
                    return NATURAIS
            else:
                if num <= 95:
                    return INGLES
                elif num <= 100:
                    return ESPANHOL
                elif num <= 140:
                    return LINGUAGENS
                else:
                    return MATEMATICA
        else:
            if day == 1:
                if num <= 5:
                    return INGLES
                elif num <= 10:
                    return ESPANHOL
                elif num <= 50:
                    return LINGUAGENS
                else:
                    return HUMANAS
            else:
                if num <= 135:
                    return NATURAIS
                else:
                    return MATEMATICA

    def number(self, occurrence_idx: int, day: int):
        num = occurrence_idx + 1
        if day == 2:
            num += 90
        if self.year < 2017 and day == 2 and num >= 96:
            return num - 5
        elif self.year >= 2017 and day == 1 and num >= 6:
            return num - 5
        return num