import os

from src.main.data import JSONExporter
from src.main.data.Config import YAMLConfig
from src.main.domain.PosProcessor import ENEMPosProcessor
from src.main.domain.Preprocessor import ENEMPreProcessor
from src.main.domain.Splitter import ENEMSplitter
from src.main.domain.Validator import Validator


class ENEMExporter:

    def __init__(self,
                 repo: JSONExporter,
                 preprocessor: ENEMPreProcessor,
                 posprocessor: ENEMPosProcessor,
                 validator: Validator,
                 splitter: ENEMSplitter
                 ):
        self.repo = repo
        self.preprocessor = preprocessor
        self.posprocessor = posprocessor
        self.validator = validator
        self.splitter = splitter
        self.amount_exported = 0

    def export(self, input_path: str, working_dir: str, config: YAMLConfig):
        output_path = working_dir + "/output.pdf"

        pre_dir = working_dir + "/preprocessor/"
        os.mkdir(pre_dir)

        self.preprocessor.linear(
            pre_dir,
            input_path,
            output_path,
            config.config["one_column_pages"],
            config.config["excluded_pages"]
        )

        results = []

        def on_next(question):
            pos_dir = working_dir + "/posprocessor/" + str(self.amount_exported + 1)
            self.amount_exported += 1
            os.makedirs(pos_dir, 0o755)
            meta = self.posprocessor.posprocess(output_path, question, pos_dir)
            results.append(meta)

        def completed():
            if self.validator.validate(results):
                for meta in results:
                    self.repo.save(meta)
            else:
                print("Error Found")

        splitter_dir = working_dir + "/splitter/"
        os.mkdir(splitter_dir)

        self.splitter.split(
            splitter_dir,
            output_path
        ).subscribe(on_next=on_next, on_completed=completed)
