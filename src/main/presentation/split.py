import os
import shutil

from src.main.data.Config import YAMLConfig
from src.main.data.JSONExporter import JSONExporter
from src.main.domain.enem.Handler import ENEMHandler
from src.main.domain.Operation import Operation
import calendar
import time
from os import listdir
from os.path import isfile, join

rootPath = "/Users/danielspeixoto/IdeaProjects/enem-parser/"
output = "/Volumes/Data/enem/experiments/"
exams = rootPath + "/exams/"
configs = [f for f in listdir(exams) if isfile(join(exams, f))]

print("Available configs")
for i in range(len(configs)):
    print(str(i) + ": " + configs[i])

opt_idx = input("Choose an option")
config = YAMLConfig(exams + configs[int(opt_idx)])

folder_id = str(calendar.timegm(time.gmtime())) + \
            str(config.config["year"]) + \
            str(config.config["day"]) + \
            str(config.config["variant"])

if not os.path.exists(output):
    os.mkdir(output)
exporter_dir = output + "/exporter"
if not os.path.exists(exporter_dir):
    os.mkdir(exporter_dir)
current_dir = exporter_dir + "/" + str(folder_id)
os.mkdir(current_dir)

json = output + "/json/" + str(config.config["year"]) + \
       "/" + str(config.config["day"]) + \
       "/" + str(config.config["variant"]) + "/"
while os.path.exists(json):
    try:
        shutil.rmtree(json)
    except:
        ""
os.makedirs(json)

repo = JSONExporter(json)
exporter = ENEMHandler(config, current_dir)
op = Operation(repo)
op.run(exporter)
