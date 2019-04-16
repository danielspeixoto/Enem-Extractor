import os
import pandas as pd
import base64

from src.main.aggregates.pdf_item import Question


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

        domain, question_idx = self._domain(question.number)

        with open(output, "rb") as pdf:
            meta = {
                "year": str(self.year),
                "source": "ENEM",
                "variant": self.variant,
                "domain": domain,
                "number": str(question_idx + 1),
                "answer": self._answer(question_idx),
                "pdf": base64.b64encode(pdf.read()).decode()
            }

            return meta

    def _domain(self, question_num: int):
        question_idx = question_num - 1
        if self.day == 2:
            question_idx += 90
        if self.year >= 2017:
            if self.day == 2:
                if question_idx < 135:
                    return "naturais", question_idx
                else:
                    return "matematica", question_idx
            else:
                if question_idx < 5:
                    return "ingles", question_idx
                elif question_idx < 10:
                    return "espanhol", question_idx - 5
                elif question_idx < 50:
                    return "linguagens", question_idx - 5
                else:
                    return "humanas", question_idx - 5
        else:
            if self.day == 2:
                if question_idx < 135:
                    return "humanas", question_idx
                else:
                    return "naturais", question_idx
            else:
                if question_idx <= 5:
                    return "ingles", question_idx
                elif question_idx <= 10:
                    return "espanhol", question_idx - 5
                elif question_idx < 50:
                    return "linguagens", question_idx - 5
                else:
                    return "matematica", question_idx - 5

    def _answer(self, question_idx: int):
        if self.year >= 2017:
            # First day had 95 questions instead of only 90
            question_idx += 5
        df = pd.read_csv(self.microdata_path, sep=";")
        df = df.loc[df['TX_COR'] == self.variant]
        ans = df.iloc[question_idx, 3]
        return ord(ans[0]) - ord('A')



