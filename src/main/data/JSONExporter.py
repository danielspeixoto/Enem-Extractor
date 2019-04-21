import json
from os import listdir
from os.path import isfile, join

class JSONExporter:

    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.amount_exported = 0

    def save(self, question):
        with open(self.storage_path + "/" +
                  str(self.amount_exported) + ".json", "w") as fp:
            self.amount_exported += 1
            json.dump(question, fp)

    def all(self):
        for file in [f for f in listdir(self.storage_path)
                     if isfile(join(self.storage_path, f))]:

            with open(self.storage_path + "/" + file, "rb") as f:
                yield json.load(f)


