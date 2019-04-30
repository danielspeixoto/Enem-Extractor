import os

from src.main.aggregates.Question import Question
import googleapiclient.discovery

from src.main.aggregates.Video import Video


class RelatedVideos:

    def __init__(self, api_keys: [str]):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.youtubes = []
        for k in api_keys:
            self.youtubes.append(
                googleapiclient.discovery.build(
                    "youtube", "v3", developerKey=k)
            )
        self.last_used = 0

        self.ALL_COLORS = ["azul", "amarel", "rosa", "cinza", "branc"]

    def youtube(self):
        return self.youtubes[self.last_used % len(self.youtubes)]

    def related(self, question: Question):
        query: str = question.source + " " + str(question.edition) + " " + \
                     question.variant + " Questão " + str(question.number) + \
                     " " + question.domain

        response = self.youtube().search().list(query).execute()

        must_have = [
            question.source.lower(),
            str(question.edition).lower(),
            question.variant.lower(),
            " " + str(question.number) + " ",
        ]
        accepted_videos = []
        for item in response["items"]:
            snippet = item["snippet"]
            title = " " + snippet["title"] + " "
            title = title.lower()

            accepted = True

            for color in self.ALL_COLORS:
                if color in title and color not in question.variant.lower():
                    accepted = False
                    break

            if accepted:
                for cond in must_have:
                    if cond not in title:
                        accepted = False
                        break

            if accepted:
                accepted_videos.append(
                    Video(

                    )
                )





