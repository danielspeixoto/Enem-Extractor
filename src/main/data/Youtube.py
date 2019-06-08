import os
import re

from src.main.aggregates.Question import Question
import googleapiclient.discovery

from src.main.aggregates.Video import Video


class Youtube:

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
        self.last_used += 1
        return self.youtubes[self.last_used % len(self.youtubes)]

    def related(self,
                question_id: str,
                source: str,
                edition: int,
                variant: str,
                number: int,
                domain: str):
        query: str = source + " " + str(edition) + " " + \
                     variant + " Questão " + str(number) + \
                     " " + domain

        response = self.youtube().search().list(
            part="snippet,id",
            maxResults=25,
            q=query
        ).execute()

        print("response ")

        must_have = [
            source.lower(),
            str(edition).lower(),
            variant.lower()[:-1],
        ]
        domain = domain.lower()
        if domain == "inglês" or domain == "espanhol":
            # Lingua (ingles)a, lingua (espanhol)a
            if domain == "inglês":
                domain = "ingles"
            must_have.append(domain)
        divider = re.compile("[\- .|qQ)(]([.]?)([0]?)" + str(number) + "[\- .|)(]")
        accepted_videos = []
        i = -1
        for item in response["items"]:
            i += 1
            snippet = item["snippet"]
            title = " " + snippet["title"] + " "
            title = title.lower()

            accepted = True

            for color in self.ALL_COLORS:
                if color in title and color not in variant.lower():
                    accepted = False
                    break

            if accepted:
                for cond in must_have:
                    if cond not in title:
                        accepted = False
                        break

            if accepted:
                if re.search(divider, title) is None:
                    accepted = False
                    break

            if accepted:
                accepted_videos.append(
                    Video(
                        snippet["title"],
                        snippet["channelTitle"],
                        snippet["channelId"],
                        snippet["thumbnails"]["default"]["url"],
                        snippet["thumbnails"]["medium"]["url"],
                        snippet["thumbnails"]["high"]["url"],
                        snippet["description"],
                        snippet["publishedAt"],
                        item["etag"],
                        item["id"]["videoId"],
                        i,
                        question_id
                    )
                )
        return accepted_videos





