from bson import ObjectId
from pymongo import MongoClient

from src.main.aggregates.Question import Question
from src.main.aggregates.Video import Video


class DB:

    def __init__(self,
                 uri: str,
                 db_name: str,
                 questions_collection: str,
                 videos_collection: str
                 ):
        client = MongoClient(uri)
        self.questions_collection = client.get_database(db_name).get_collection(questions_collection)
        self.videos_collection = client.get_database(db_name).get_collection(videos_collection)

    def has_not_searched_videos(self, year: int = -1):
        if year != -1:
            cursor = self.questions_collection.find({
                "hasSearchedForVideos": {
                    "$ne": True
                },
                "year": year
            })
        else:
            cursor = self.questions_collection.find({
                "hasSearchedForVideos": {
                    "$ne": True
                }
            })
        for doc in cursor:
            yield Question(
                str(doc["_id"]),
                doc["source"],
                doc["variant"],
                doc["edition"],
                doc["number"],
                doc["itemCode"],
                doc["domain"],
                doc["stage"]
            )

    def mark_has_searched(self, question: Question):
        self.questions_collection.find_one_and_update({
            "_id": ObjectId(question.id)
        }, {
            "$set": {
                "hasSearchedForVideos": True
            }
        })

    def insert_video(self, videos: [Video]):
        docs = []
        for video in videos:
            docs.append({
                "title": video.title,
                "channel": {
                    "title": video.channelTitle,
                    "id": video.channelId
                },
                "thumbnails": {
                    "high": video.high_thumbnail,
                    "medium": video.medium_thumbnail,
                    "default": video.default_thumbnail
                },
                "description": video.description,
                "publishedAt": video.published_at,
                "etag": video.etag,
                "videoId": video.videoId,
                "retrievalPosition": video.retrievalPosition,
                "questionId": ObjectId(video.questionId)
            })
        self.videos_collection.insert_many(docs)

    def has_exam(self, year: int, day: int):
        count = self.questions_collection.count({
            "edition": year,
            "stage": day
        })
        return count > 0
