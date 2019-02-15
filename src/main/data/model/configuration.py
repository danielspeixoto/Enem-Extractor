import errno
import os

from data.repository.PickleRepository import PickleRepository

class Environment:

    def __init__(self, config_path=""):
        self.enem_path = "/home/daniel/Documents/enem/2016-2.pdf"
        self.microdata_path = "/home/daniel/Documents/enem/microdados_enem2016/DADOS/itens_prova_2016.csv"
        self.amount_of_questions = 95
        self.one_column_pages = [24, 27]
        self.excluded_pages = [
            # Front page
            0,
            1,
            # Dissertation instructions
            # 18,
            # Dissertation
            31
        ]
        self.metadata = {
            "year": 2016,
            "day": 2,
            "color": "AZUL"
        }



        self.working_dir = "/home/daniel/work/enem-parser/data/"
        # Fixed value, TODO: Use project location reference
        self.res_folder = "/home/daniel/work/enem-parser/res/"
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