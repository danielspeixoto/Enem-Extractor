import json


class JSONExporter:

    def __init__(self, storage_path):
        self.storage_path = storage_path

    def save(self, question):
        with open(self.storage_path + "/" +
                  str(question["number"]) + ".json", "w") as fp:
            json.dump(question, fp)
