import os

from src.main.data.Config import YAMLConfig
from src.main.data.JSONExporter import JSONExporter
from src.main.domain.Exporter import ENEMExporter
from src.main.domain.PosProcessor import ENEMPosProcessor
from src.main.domain.Preprocessor import ENEMPreProcessor
from src.main.domain.Splitter import ENEMSplitter

output = "/Users/danielspeixoto/experiments/enem-parser"

config = YAMLConfig("/Users/danielspeixoto/IdeaProjects/enem-parser/config.yaml")
input_path = config.config["input"]

json = output + "/json"
os.mkdir(json, 0o755)
repo = JSONExporter(json)

preprocessor = ENEMPreProcessor()

splitter = ENEMSplitter("/Users/danielspeixoto/IdeaProjects/enem-parser/src/res/question_pattern.png")

posprocessor = ENEMPosProcessor(
    input_path,
    config.config["year"],
    config.config["day"],
    config.config["variant"],
    config.config["micro_data"],
)

exporter = ENEMExporter(repo, preprocessor, posprocessor, splitter)

exporter_dir = output + "/exporter"
os.mkdir(exporter_dir, 0o755)
exporter.export(input_path, exporter_dir, config)