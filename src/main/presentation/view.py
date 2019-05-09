import base64
import io

from PIL import Image

from main.data.DB import DB

db = DB(
    "mongodb+srv://enemparser:IqTqmHxP4tHyCYxK@cluster0-lf760.mongodb.net/test?retryWrites=true",
    "heroku_wn1s1nxv",
    "questions",
    "relatedVideos"
)
view = ""
for a in db.id("5cc928972cb8fec8b784c86b"):
    view = a.view
data_img = base64.b64decode(view)
img = Image.open(io.BytesIO(data_img))
img.show()