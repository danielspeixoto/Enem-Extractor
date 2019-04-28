import os
import shutil
import sys

import base64

from PIL import Image

from src.main.data.Config import YAMLConfig
from src.main.data.JSONExporter import JSONExporter
from src.main.domain.Exporter import ENEMExporter
from src.main.domain.PosProcessor import ENEMPosProcessor
from src.main.domain.Preprocessor import ENEMPreProcessor
from src.main.domain.Splitter import ENEMSplitter
from src.main.domain.Validator import Validator


output = "/Volumes/Data/enem/experiments/"
if not os.path.exists(output):
    os.mkdir(output)

exporter_dir = output + "/exporter"
while os.path.exists(exporter_dir):
    try:
        shutil.rmtree(exporter_dir)
    except:
        ""
os.mkdir(exporter_dir)

rootPath = "/Users/danielspeixoto/IdeaProjects/enem-parser"
print(rootPath)

config = YAMLConfig(rootPath + "/exams/16-2-amarelo.yaml")
input_path = config.config["input"]

json = output + "/json/" + \
       str(config.config["year"]) + \
       "/" + str(config.config["day"]) + \
       "/" + str(config.config["variant"])
while os.path.exists(json):
    try:
        shutil.rmtree(json)
    except:
        ""
os.makedirs(json, 0o755)
repo = JSONExporter(json)

preprocessor = ENEMPreProcessor()

splitter = ENEMSplitter(rootPath + "/src/res/question_pattern.png")

posprocessor = ENEMPosProcessor(
    config.config["year"],
    config.config["day"],
    config.config["variant"],
    config.config["micro_data"],
)

validator = Validator(
    config.config["year"],
    config.config["day"],
    config.config["variant"],
    config.config["micro_data"],
)

exporter = ENEMExporter(repo, preprocessor, posprocessor, validator, splitter)
exporter.export(input_path, exporter_dir, config)
