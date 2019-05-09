import base64
import io

from PIL import Image

from main.aggregates.Question import Question

def question_view_size(question: Question):
    print("size")
    view = str(question.view)
    data_img = base64.b64decode(view)
    img = Image.open(io.BytesIO(data_img))
    return img.size
