import os
import shutil

from src.main.data.Config import YAMLConfig
from src.main.data.JSONExporter import JSONExporter
from src.main.data.MicroData import MicroData
from src.main.domain.enem.Handler import ENEMHandler
from src.main.domain.enem.PosProcessor import ENEMPosProcessor
from src.main.domain.enem.PreProcessor import ENEMPreProcessor
from src.main.domain.enem.Splitter import ENEMSplitter
from src.main.domain.enem.Validator import ENEMValidator
from src.main.domain.Operation import Operation
import calendar
import time

rootPath = "/Users/danielspeixoto/IdeaProjects/enem-parser"
config = YAMLConfig(rootPath + "/exams/14-2-azul.yaml")
# info = str(config.config["year"]) + " " + str(config.config["day"]) + " " + str(config.config["variant"])
# print(info)

folder_id = str(calendar.timegm(time.gmtime())) + \
            str(config.config["year"]) + \
            str(config.config["day"]) + \
            str(config.config["variant"])

output = "/Volumes/Data/enem/experiments/"
if not os.path.exists(output):
    os.mkdir(output)
exporter_dir = output + "/exporter"
if not os.path.exists(exporter_dir):
    os.mkdir(exporter_dir)
current_dir = exporter_dir + "/" + str(folder_id)
if not os.path.exists(current_dir):
    os.mkdir(current_dir)

json = output + "/json/"
while os.path.exists(json):
    try:
        shutil.rmtree(json)
    except:
        ""
os.makedirs(json, 0o755)
repo = JSONExporter(json)
exporter = ENEMHandler(config)

op = Operation(repo, exporter, current_dir)
op.run()
