import os

from src.main.data import JSONExporter
from src.main.data.Config import YAMLConfig
from src.main.domain.PosProcessor import ENEMPosProcessor
from src.main.domain.Preprocessor import ENEMPreProcessor
from src.main.domain.Splitter import ENEMSplitter


class ENEMExporter:

    def __init__(self,
                 repo: JSONExporter,
                 preprocessor: ENEMPreProcessor,
                 posprocessor: ENEMPosProcessor,
                 splitter: ENEMSplitter
                 ):
        self.repo = repo
        self.preprocessor = preprocessor
        self.posprocessor = posprocessor
        self.splitter = splitter

    def export(self, input_path: str, working_dir: str, config: YAMLConfig):
        output_path = working_dir + "/output.pdf"

        self.preprocessor.linear(
            working_dir + "/preprocessor/",
            input_path,
            output_path,
            config.config["one_column_pages"],
            config.config["excluded_pages"]
        )

        def on_next(question):
            pos_dir = working_dir + "/" + str(question.number)
            os.mkdir(pos_dir, 0o755)
            meta = self.posprocessor.posprocess(question, pos_dir)
            self.repo.save(meta)

        self.splitter.split(
            working_dir + "/splitter/",
            output_path
        ).subscribe(on_next=on_next)
