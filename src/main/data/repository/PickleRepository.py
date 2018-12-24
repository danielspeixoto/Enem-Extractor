import datetime
import errno
import os
import pickle

class PickleRepository:

    def __init__(self, data_path):
        self._data_path = data_path
        self._questions_path = self._data_path + "/questions"
        self._is_open = False
        self.file = None

    def all(self):
        questions = PickleRepository._load_obj(self._questions_path)
        return questions

    def save(self, questions):
        if self.file is None:
            print("Creating file")
            self.file = PickleRepository._create(self._questions_path)
        self._write(self.file, questions)

    def close(self):
        self.file.close()

    @staticmethod
    def _write(pkl_file, questions):
        pickle.dump(questions, pkl_file, protocol=2)

    @staticmethod
    def _load_obj(path):
        with open(path + '.pkl', 'rb') as f:
            while True:
                try:
                    for obj in pickle.load(f):
                        yield obj
                except EOFError:
                    break

    @staticmethod
    def _create(path):
        path = path + ".pkl"
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        # if os.path.isfile(path):
        #     return PickleRepository._create(path + str(
        #         datetime.datetime.now()))

        return open(path, "wb+")