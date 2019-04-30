from src.main.data.DB import DB
from src.main.data.MicroData import ENEMInfo
from src.main.data.Youtube import Youtube


class RelatedVideos:

    def __init__(self, db: DB, youtube: Youtube, info: ENEMInfo):
        self.db = db
        self.youtube = youtube
        self.info = info

    def get(self):
        questions = self.db.has_not_searched_videos()
        for q in questions:
            variants = self.info.variants(q.edition, q.item_code)
            if len(variants) == 0:
                continue
            for v in variants:
                if q.variant[:-1] in v[0]:
                    if q.number != v[1]:
                        print("variants inconsistency")
                        print(q)
                        print(variants)
                        exit(1)
            for v in variants:
                videos = self.youtube.related(
                    q.id,
                    q.source,
                    q.edition,
                    v[0],
                    v[1],
                    q.area_number
                )
                if len(videos) > 0:
                    self.db.insert_video(videos)
                    break
            self.db.mark_has_searched(q)
