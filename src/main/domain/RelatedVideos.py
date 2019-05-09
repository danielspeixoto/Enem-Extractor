from src.main.data.DB import DB
from src.main.data.MicroData import ENEMInfo
from src.main.data.Youtube import Youtube


class RelatedVideos:

    def __init__(self, db: DB, youtube: Youtube, info: ENEMInfo):
        self.db = db
        self.youtube = youtube
        self.info = info

    def get(self):
        not_found = 0
        questions = self.db.has_not_searched_videos()
        amount = 0
        for q in questions:
            amount += 1
            print("Processing: " + str(q.edition) + " " + str(q.number) + " " + str(q.variant) + " " + str(q.domain))
            variants = self.info.variants(q.edition, q.item_code)
            if len(variants) == 0:
                print("No variants, should have variants")
                print(q)
                exit(1)
            for v in variants:
                if q.variant[:-1].lower() in v[0].lower():
                    if q.number != v[1]:
                        print("variants inconsistency")
                        print(q)
                        print(variants)
                        exit(1)
            found = False
            for v in variants:
                videos = self.youtube.related(
                    q.id,
                    q.source,
                    q.edition,
                    v[0],
                    v[1],
                    q.domain
                )
                if len(videos) > 0:
                    self.db.insert_video(videos)
                    found = True
                    break
            if not found:
                print(str(q.number) + " has no videos")
                not_found += 1
            self.db.mark_has_searched(q)
            # if amount > 0:
            #     print("Year: " + str(year) + " " + str(not_found/float(amount)) + " has no videos")
