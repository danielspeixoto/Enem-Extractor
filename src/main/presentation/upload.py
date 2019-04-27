import json
import time

from src.main.data.Config import YAMLConfig
from src.main.data.JSONExporter import JSONExporter
import requests

output = "/Volumes/Data/enem/experiments/"

config = YAMLConfig("/Users/danielspeixoto/IdeaProjects/enem-parser/exams/16-2-amarelo.yaml")

jsonRepo = output + "/json/" + \
           str(config.config["year"]) + \
           "/" + str(config.config["day"]) + \
           "/" + str(config.config["variant"])
repo = JSONExporter(jsonRepo)

# url = "http://localhost:5000/questions/"
url = "https://protected-river-16209.herokuapp.com/question/"
i = 0
for q in repo.all():
    r = requests.post(url, data=json.dumps(q))
    if r.status_code != 200:
        print("Failed")
        print(r.reason)
        exit(1)
    i += 1
    print(str(i) + " Questions uploaded")
