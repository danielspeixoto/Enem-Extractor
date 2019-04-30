from flask import Flask, render_template, url_for
from flask import request
import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

rootPath = "/Users/danielspeixoto/IdeaProjects/enem-parser"
exams = rootPath + "/exams"

output = "/Volumes/Data/enem/experiments/"
if not os.path.exists(output):
    os.mkdir(output)
exporter_dir = output + "/exporter"
if not os.path.exists(exporter_dir):
    os.mkdir(exporter_dir)
current_dir = exporter_dir + "/" + str(folder_id)
if not os.path.exists(current_dir):
    os.mkdir(current_dir)

json_output = output + "/json/"

@app.route("/")
@cross_origin()
def home():
    return render_template('home.html')

@app.route("/process/<exam>")
@cross_origin()
def process(exam: str):
    return render_template('process.html')

@app.route("/upload/<exam>")
@cross_origin()
def upload(exam: str):
    return render_template('process.html')


app.run(port=3000, host='0.0.0.0')