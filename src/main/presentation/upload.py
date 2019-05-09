import json
import time
from os import listdir
from os.path import isfile, join

from main.data.DB import DB
from src.main.data.JSONExporter import JSONExporter
import requests

output = "/Volumes/Data/enem/experiments/"
json_dir = output + "json/"

db = DB(
    "mongodb+srv://enemparser:IqTqmHxP4tHyCYxK@cluster0-lf760.mongodb.net/test?retryWrites=true",
    "heroku_wn1s1nxv",
    "questions",
    "relatedVideos"
)

print("Loading available options...")
options = []
years = [f for f in listdir(json_dir) if join(json_dir, f)]
for year in years:
    year_path = json_dir + year + "/"
    days = [f for f in listdir(year_path) if join(year_path, f)]
    for day in days:
        day_path = year_path + day + "/"
        if not db.has_exam(int(year), int(day)):
            variants = [f for f in listdir(day_path) if join(day_path, f)]
            for v in variants:
                v_path = day_path + v + "/"
                data = [f for f in listdir(v_path) if join(v_path, f)]
                if len(data) >= 90:
                    print(str(len(options)) + ": " + year + " " + day + " " + v)
                    options.append(v_path)

if len(options) == 0:
    print("No options available")
    exit(0)
opt_idx = input("Choose an option")

repo = JSONExporter(options[int(opt_idx)])

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
