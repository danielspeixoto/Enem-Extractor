import os
from typing import Dict

from rx import Observable

from main.data.MicroData import MicroData
from src.main.data.Config import YAMLConfig
from src.main.domain.enem.PosProcessor import ENEMPosProcessor
from src.main.domain.enem.PreProcessor import ENEMPreProcessor
from src.main.domain.enem.Splitter import ENEMSplitter
from src.main.domain.enem.Validator import ENEMValidator


class ENEMHandler:

    def __init__(self,
                 config: YAMLConfig,
                 working_dir: str,
                 ):
        self.working_dir = working_dir
        self.temp_path = working_dir + "/temp.pdf"
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

        self.pos_dir = self.working_dir + "/posprocessor/"
        os.mkdir(self.pos_dir)

    def pre_process(self):
        pre_dir = self.working_dir + "/preprocessor/"
        os.mkdir(pre_dir)
        self.preprocessor.linear(
            pre_dir,
            self.config["input"],
            self.temp_path,
            self.config["one_column_pages"],
            self.config["excluded_pages"],
            self.config["year"]
        )

    def split(self)-> Observable:
        split_dir = self.working_dir + "/splitter/"
        os.mkdir(split_dir)
        return self.splitter.split(
            split_dir,
            self.temp_path
        )

    def pos_process(self, question)-> Dict:
        self.amount_exported += 1
        path = self.pos_dir + "/" + str(self.amount_exported)
        os.mkdir(path)
        meta = self.posprocessor.pos_process(self.temp_path, question, path)
        return meta

    def validate(self, questions)-> bool:
        return self.validator.validate(questions)