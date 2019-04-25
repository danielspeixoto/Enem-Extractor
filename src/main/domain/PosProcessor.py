import os
import pandas as pd
import base64

from src.main.aggregates.pdf_item import Question
from src.main.domain.Vision import pdf2img, pdf2multiple_img


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
        self.microdata_path = micro_data_path

    def posprocess(self,
                   pdf_input_path, question: Question, working_dir):
        question_folder = working_dir + "/question/"
        os.mkdir(question_folder, 0o755)

        output = working_dir + "/out.pdf"
        question.save_as_pdf(pdf_input_path, question_folder, output)

        output_img = working_dir + "/out.jpg"

        img_dir = working_dir + "/img/"
        os.mkdir(img_dir)
        pdf2multiple_img(img_dir, output, output_img, 250)

        domain, question_num = self._domain(question.occurrence_idx)

        with open(output_img, "rb") as file:
            meta = {
                "edition": self.year,
                "source": "ENEM",
                "variant": self.variant,
                "domain": domain,
                "number": question_num,
                "answer": self._answer(question.occurrence_idx),
                "pdf": base64.b64encode(file.read()).decode(),
                "referenceId": str(self._reference_id(question.occurrence_idx)),
                "tags": []
            }

            return meta

    def _domain(self, occurrence_idx: int):
        num = occurrence_idx + 1
        if self.day == 2:
            num += 90
        if self.year >= 2017:
            if self.day == 2:
                if num <= 135:
                    return "naturais", num
                else:
                    return "matemática", num
            else:
                if num <= 5:
                    return "inglês", num
                elif num <= 10:
                    return "espanhol", num - 5
                elif num <= 50:
                    return "linguagens", num - 5
                else:
                    return "humanas", num - 5
        else:
            if self.day == 2:
                if num <= 95:
                    return "ingles", num
                elif num <= 100:
                    return "espanhol", num - 5
                elif num <= 140:
                    return "linguagens", num - 5
                else:
                    return "matematica", num - 5
            else:
                if num <= 45:
                    return "humanas", num
                else:
                    return "naturais", num

    def _answer(self, question_idx: int):
        if self.day == 2:
            question_idx += 90
        if self.year >= 2017:
            # First day had 95 questions instead of only 90
            question_idx += 5
        df = pd.read_csv(self.microdata_path, sep=";")
        df = df.loc[df['TX_COR'] == self.variant]
        ans = df.iloc[question_idx, 3]
        return ord(ans[0]) - ord('A')

    def _reference_id(self, question_idx: int):
        if self.day == 2:
            question_idx += 90
        if self.year >= 2017:
            # First day had 95 questions instead of only 90
            question_idx += 5
        df = pd.read_csv(self.microdata_path, sep=";")
        df = df.loc[df['TX_COR'] == self.variant]
        ans = df.iloc[question_idx, 2]
        return ans
