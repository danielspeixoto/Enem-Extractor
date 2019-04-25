import json
from os import listdir
from os.path import isfile, join

import io
from numpy import unicode


class JSONExporter:

    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.amount_exported = 0

    def save(self, question):
        with io.open(self.storage_path + "/" +
                     str(self.amount_exported + 1) + ".json",
                     "w", encoding='utf8') as fp:
            self.amount_exported += 1
            json.dump(question, fp, ensure_ascii=False)

    def all(self):
        for file in [f for f in listdir(self.storage_path)
                     if isfile(join(self.storage_path, f))]:
            with open(self.storage_path + "/" + file, "rb") as f:
                yield json.load(f)
