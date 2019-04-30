import os

import pandas as pd
import base64

from src.main.aggregates.pdf_item import Question
from src.main.data.MicroData import MicroData
from src.main.domain.splitter.Vision import pdf2multiple_img

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
                 micro_data_path: str
                 ):
        self.year = year
        self.day = day
        self.variant = variant
        self.micro = MicroData(micro_data_path, self.year)

    def posprocess(self,
                   pdf_input_path, question: Question, working_dir):
        question_folder = working_dir + "/question/"
        os.mkdir(question_folder, 0o755)

        output = working_dir + "/out.pdf"
        question.save_as_pdf(pdf_input_path, question_folder, output)

        output_img = working_dir + "/out.jpg"

        img_dir = working_dir + "/img/"
        os.mkdir(img_dir)
        pdf2multiple_img(img_dir, output, output_img)

        domain, question_num = self._domain(question.occurrence_idx)
        ref, ans = self._reference_id(question.occurrence_idx)

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

    def _domain(self, occurrence_idx: int):
        return self.micro.area_number(self.day, occurrence_idx)

    def _reference_id(self, occurrence_idx: int):
        return self.micro.info(occurrence_idx, self.day, self.variant)