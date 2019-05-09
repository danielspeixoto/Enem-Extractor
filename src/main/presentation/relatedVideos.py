from src.main.data.DB import DB
from src.main.data.MicroData import ENEMInfo
from src.main.data.Youtube import Youtube
from src.main.domain.RelatedVideos import RelatedVideos

db = DB(
    "mongodb+srv://enemparser:IqTqmHxP4tHyCYxK@cluster0-lf760.mongodb.net/test?retryWrites=true",
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
# info.add(2013, "/Volumes/Data/enem/microdados/Microdados_Enem_2013/PLANILHAS/ITENS_ENEM_2013.xlsx")
info.add(2012, "/Volumes/Data/enem/microdados/microdados_enem2012/DADOS/ITENS_ENEM_2012.csv")
# info.add(2015, "/Volumes/Data/enem/microdados/microdados_enem2015/PLANILHAS/ITENS_ENEM_2015.xlsx")

op = RelatedVideos(db, youtube, info)
op.get()