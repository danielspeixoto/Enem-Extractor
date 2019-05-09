from multiprocessing.pool import Pool
from functools import partial
from main.data.DB import DB


db = DB(
    "mongodb+srv://enemparser:IqTqmHxP4tHyCYxK@cluster0-lf760.mongodb.net/test?retryWrites=true",
    "heroku_wn1s1nxv",
    "questions",
    "relatedVideos"
)


def x(func, question):
    print("Processing...")
    width, height = func(question)
    db.update(question, width, height)
    return question

class BatchUpdate:

    def __init__(self, db: DB):
        self.db = db

    def map(self, func):
        questions = self.db.no_dimensions()
        m = partial(x, func)
        p = Pool(10)
        p.map(m, questions)