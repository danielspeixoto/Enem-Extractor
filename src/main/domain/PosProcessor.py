import os
import pandas as pd
import base64

from src.main.aggregates.pdf_item import Question
from src.main.domain.Vision import pdf2img, pdf2multiple_img

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
        ref, ans = self._reference_id(question.occurrence_idx)

        tags = [domain.lower()]

        with open(output_img, "rb") as file:
            meta = {
                "edition": self.year,
                "stage": self.day,
                "source": "ENEM",
                "variant": self.variant,
                "domain": domain,
                "number": question_num,
                "answer": ans,
                "view": base64.b64encode(file.read()).decode(),
                "itemCode": str(ref),
                "tags": tags,
                "referenceId": "ENEM-" + str(self.year) + "-" + str(self.day) + "-" + str(question.occurrence_idx)
            }

            return meta

    def _domain(self, occurrence_idx: int):
        num = occurrence_idx + 1
        if self.day == 2:
            num += 90
        if self.year >= 2017:
            if self.day == 2:
                if num <= 135:
                    return NATURAIS, num
                else:
                    return MATEMATICA, num
            else:
                if num <= 5:
                    return INGLES, num
                elif num <= 10:
                    return ESPANHOL, num - 5
                elif num <= 50:
                    return LINGUAGENS, num - 5
                else:
                    return HUMANAS, num - 5
        else:
            if self.day == 2:
                if num <= 95:
                    return INGLES, num
                elif num <= 100:
                    return ESPANHOL, num - 5
                elif num <= 140:
                    return LINGUAGENS, num - 5
                else:
                    return MATEMATICA, num - 5
            else:
                if num <= 45:
                    return HUMANAS, num
                else:
                    return NATURAIS, num

    def _reference_id(self, occurrence_idx: int):

        domain = "LC"
        num = occurrence_idx + 1
        if self.year >= 2017:
            if self.day == 2:
                if num <= 45:
                    domain = "CN"
                else:
                    domain = "MT"
            elif num >= 51:
                domain = "CH"
        else:
            if self.day == 2:
                if num >= 51:
                    domain = "MT"
            elif self.day == 1:
                if num <= 45:
                    domain = "CH"
                else:
                    domain = "CN"

        mod = 45
        if (self.year < 2017 and self.day == 2) or (self.year >= 2017 and self.day == 1):
            mod = 50

        idx = (occurrence_idx % mod)
        fmt = self.microdata_path.split(".")[1]
        if fmt == "csv":
            df = pd.read_csv(self.microdata_path, sep=";")
            df = df.loc[df['TX_COR'] == self.variant]
            df = df.loc[domain in df['SG_AREA']]
            ref = df.iloc[idx, 2]
            ans = df.iloc[idx, 3]
            ans = ord(ans[0]) - ord('A')
        else:
            # if self.variant != "AZUL":
            #     print(self.variant + " not supported")
            #     exit(1)
            domain += "T"
            df = pd.read_excel(self.microdata_path, sheet_name=domain)
            ref = df.iloc[idx, 4]
            ans = ord(df.iloc[idx, 5]) - ord('A')
        return ref, ans
