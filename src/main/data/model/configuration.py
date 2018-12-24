import errno
import os

from data.repository.PickleRepository import PickleRepository

class Environment:

    def __init__(self, config_path=""):
        self.enem_path = "/home/daniel/Documents/enem/2017-2.pdf"
        self.microdata_path = "/home/daniel/Documents/enem/microdados_enem2017/DADOS/ITENS_PROVA_2017.csv"
        self.amount_of_questions = 90
        self.one_column_pages = [2, 5, 10, 11, 13, 20, 26, 28]
        self.excluded_pages = [
            # Front page
            0,
            # Dissertation instructions
            # 18,
            # Dissertation
            31
        ]
        self.metadata = {
            "year": 2017,
            "day": 2,
            "color": "AZUL"
        }



        self.working_dir = "/home/daniel/PycharmProjects/enem-parser/data/"
        # Fixed value, TODO: Use project location reference
        self.res_folder = "/home/daniel/PycharmProjects/enem-parser/res/"
        # Defined by previous attributes
        self.question_pattern = self.res_folder + "/question_pattern.png"
        self.working_pdf = self.working_dir + "working.pdf"
        self.question_folder = self.working_dir + "/questions/"
        self.upload_pdf = self.working_dir + "upload.pdf"
        self._create_folder(self.question_folder)
        self.filter_path = self.working_dir + "filter.pdf"
        self.repo = PickleRepository(self.working_dir + "/pickle/")

    @staticmethod
    def _create_folder(path):
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise