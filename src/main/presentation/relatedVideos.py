from src.main.data.DB import DB
from src.main.data.MicroData import ENEMInfo
from src.main.data.Youtube import Youtube
from src.main.domain.RelatedVideos import RelatedVideos

db = DB(
    "mongodb://server:YddR97RESWA5KwN@ds047448.mlab.com:47448/heroku_wn1s1nxv",
    "heroku_wn1s1nxv",
    "questions",
    "relatedVideos"
)

youtube = Youtube(
    [
        "AIzaSyCDH_-bK082drQl4dENR_eGYyRmS4Na7zQ",
        "AIzaSyAb43-skjXjCx6YjzgXQ3rMfn9pbBPKpag",
        "AIzaSyDrEvdW_Hu-0BtqmciIow-q14shuKxhhXc",
        "AIzaSyCYvwIEVDJpL89W6qqEbI_EyVVijC_6e2Q"
    ]
)

info = ENEMInfo()
# info.add(2014, "/Volumes/Data/enem/microdados/microdados_enem2014/PLANILHAS/ITENS_ENEM_2014.xlsx")
info.add(2015, "/Volumes/Data/enem/microdados/microdados_enem2015/PLANILHAS/ITENS_ENEM_2015.xlsx")

op = RelatedVideos(db, youtube, info)

op.get()