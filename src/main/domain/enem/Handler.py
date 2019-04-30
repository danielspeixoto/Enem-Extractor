import os

from src.main.data import JSONExporter
from src.main.data.Config import YAMLConfig
from src.main.domain.enem.PosProcessor import ENEMPosProcessor
from src.main.domain.enem.PreProcessor import ENEMPreProcessor
from src.main.domain.enem.Splitter import ENEMSplitter
from src.main.domain.enem.Validator import ENEMValidator


class ENEMHandler:

    def __init__(self,
                 config: YAMLConfig,
                 ):
        self.config = config.config
        micro = MicroData(
            config.config["micro_data"],
            config.config["year"]
        )
        d = config.config
        self.preprocessor = ENEMPreProcessor()
        self.posprocessor = ENEMPosProcessor(
            d["year"],
            d["day"],
            d["variant"],
            micro
        )
        self.validator = ENEMValidator(
            d["year"],
            d["day"],
            d["variant"],
            micro
        )
        self.splitter = ENEMSplitter()
        self.amount_exported = 0

    def pre_process(self, output_path, working_dir):
        self.preprocessor.linear(
            working_dir,
            self.config["input"],
            output_path,
            config.config["one_column_pages"],
            config.config["excluded_pages"],
            config.config["year"]
        )

    def split(self, input_path, working_dir)-> Observable:
        return self.splitter.split(
            working_dir,
            input_path
        )

    def pos_process(self, question, working_dir)-> Dict:
        meta = self.posprocessor.pos_process(output_path, question, working_dir)
        return meta

    def validate(self, questions)-> bool:
        return self.validator.validate(questions)