import os
import pandas as pd
import base64

from src.main.aggregates.pdf_item import Question
from src.main.domain.Vision import pdf2img, pdf2multiple_img

INGLES = "Inglês"
ESPANHOL = "Espanhol"
LC = "Linguagens"
MT = "matemática"
CH = "humanas"
CN = "naturais"


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
        print(domain)
        ref, ans = self._reference_id(question.occurrence_idx)

        tags = [domain.lower()]

        with open(output_img, "rb") as file:
            meta = {
                "edition": self.year,
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
                    return CN, num
                else:
                    return MT, num
            else:
                if num <= 5:
                    return INGLES, num
                elif num <= 10:
                    return ESPANHOL, num - 5
                elif num <= 50:
                    return LC, num - 5
                else:
                    return CH, num - 5
        else:
            if self.day == 2:
                if num <= 95:
                    return INGLES, num
                elif num <= 100:
                    return ESPANHOL, num - 5
                elif num <= 140:
                    return LC, num - 5
                else:
                    return MT, num - 5
            else:
                if num <= 45:
                    return CH, num
                else:
                    return CN, num

    def _reference_id(self, occurrence_idx: int):
        df = pd.read_csv(self.microdata_path, sep=";")
        df = df.loc[df['TX_COR'] == self.variant]

        domain = "LC"
        num = occurrence_idx + 1
        if self.year >= 2017:
            if self.day == 2:
                if num <= 135:
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

        df = df.loc[df['SG_AREA'] == domain]

        mod = 45
        print(domain)
        if (domain == "LC") or \
                (self.year < 2017 and self.day == 2):
            mod = 50

        loc = (occurrence_idx % mod)
        print(loc)

        ref = df.iloc[loc, 2]
        ans = df.iloc[loc, 3]
        return ref, ord(ans[0]) - ord('A')
