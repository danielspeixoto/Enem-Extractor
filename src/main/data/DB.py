from pymongo import MongoClient

from src.main.aggregates.Question import Question


class DB:

    def __init__(self, uri: str, db_name: str, collection: str):
        client = MongoClient(uri)
        self.collection = client.get_database(db_name).get_collection(collection)

    def has_not_searched_videos(self):
        cursor = self.collection.find({
            "hasSearchedForVideos": False
        })
        for doc in cursor:
            yield Question(
                doc["source"],
                doc["variant"],
                doc["edition"],
                doc["number"],
                doc["itemCode"],
                doc["domain"],
                doc["stage"]
            )
