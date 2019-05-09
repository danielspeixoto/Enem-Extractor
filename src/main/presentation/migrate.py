import pymongo

from main.aggregates.Question import Question
from main.data.DB import DB
from main.domain.BatchUpdate import BatchUpdate
from main.domain.ImageSize import question_view_size

db = DB(
    "mongodb+srv://enemparser:IqTqmHxP4tHyCYxK@cluster0-lf760.mongodb.net/test?retryWrites=true",
    "heroku_wn1s1nxv",
    "questions",
    "relatedVideos"
)

b = BatchUpdate(db)

b.map(question_view_size)
