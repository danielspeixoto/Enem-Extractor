import cv2
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
from pyPdf import PdfFileReader

from util.vision import image, pdf_utils

enem_path = "/home/daniel/Documents/enem/a.pdf"
output_path = "/home/daniel/PycharmProjects/enem-parser/data/contoured.jpg"

img_path = "/home/daniel/PycharmProjects/enem-parser/data/out.jpg"

file = "/home/daniel/PycharmProjects/enem-parser/data/working.pdf"
file = enem_path
helper = "/home/daniel/PycharmProjects/enem-parser/data/helper.pdf"

pdf_utils.copy_page(file, helper, 25)

image.pdf2img(helper, img_path)

m_image = cv2.imread(img_path)
_, i_y = image.size(img_path)
# i_y -= 200

def convert_y(position, height):
    position = height - position
    return convert(position, height)

def convert(position, height):
    return int(i_y * position / height)


def parse_obj(lt_objs, mediabox):
    hei = mediabox[3] - mediabox[1]
    lower = mediabox[0], mediabox[1]
    upper = mediabox[2], mediabox[3]
    # loop over the object list
    for obj in lt_objs:
        # if lower[0] <= obj.bbox[0] + lower[0] <= upper[0] and lower[0] <= obj.bbox[2] + lower[0] <= upper[0] and lower[1] <= obj.bbox[1] + lower[1] <= \
        #         upper[1] and lower[1] <= obj.bbox[3] + lower[1] <= upper[1]:
            ww = 50
            if False:
                pass
            # elif isinstance(obj, pdfminer.layout.LTImage):
            #     color = (255, 0, 0)
            #     y = int(convert_y(obj.bbox[1], hei))
            #     x = int(convert(obj.bbox[0], hei))
            #     w = int(convert(obj.width, hei))
            #     h = int(convert(obj.height, hei))
            #     # if w > 100 and h > 300 and y < 5000:
            #     cv2.rectangle(m_image, (x, y), (x + w, y - h), color, ww)
            elif isinstance(obj, pdfminer.layout.LTFigure):
                color = (0, 0, 255)
                y = int(convert_y(obj.bbox[1], hei)) + mediabox[1]
                x = int(convert(obj.bbox[0], hei)) + mediabox[0]
                w = int(convert(obj.width, hei))
                h = int(convert(obj.height, hei))

                cv2.rectangle(m_image, (x, y), (x + w, y - h), color, ww)
            # elif isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            #     color = (0, 0, 255)
            #     y = int(convert_y(obj.bbox[1], hei)) + mediabox[1]
            #     x = int(convert(obj.bbox[0], hei)) + mediabox[0]
            #     w = int(convert(obj.width, hei))
            #     h = int(convert(obj.height, hei))
            #     if w < 1000 and h < 100:
            #         cv2.rectangle(m_image, (x, y), (x + w, y - h), color, ww)
            # elif isinstance(obj, pdfminer.layout.LTTextBoxVertical):
            #     color = (0, 0, 255)
            #     y = int(convert_y(obj.bbox[1], hei)) + mediabox[1]
            #     x = int(convert(obj.bbox[0], hei)) + mediabox[0]
            #     w = int(convert(obj.width, hei))
            #     h = int(convert(obj.height, hei))
            #     if h < 100 and w < 50:
            #         cv2.rectangle(m_image, (x, y), (x + w, y - h), color, ww)
            # elif isinstance(obj, pdfminer.layout.LTCurve):
            #     color = (0, 255, 0)
            #     y = int(convert_y(obj.bbox[1], hei)) + mediabox[1]
            #     x = int(convert(obj.bbox[0], hei)) + mediabox[0]
            #     w = int(convert(obj.width, hei))
            #     h = int(convert(obj.height, hei))
            #     if (h < 2000):
            #         cv2.rectangle(m_image, (x, y), (x + w, y - h), color, ww)
            elif isinstance(obj, pdfminer.layout.LTContainer) and not isinstance(obj, pdfminer.layout.LTTextBox):
                parse_obj(obj._objs, mediabox)

# Open a PDF file.
fp = open(helper, 'rb')

# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)

# Create a PDF document object that stores the document structure.
# Password for initialization as 2nd parameter
document = PDFDocument(parser)

# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()

# Create a PDF device object.
device = PDFDevice(rsrcmgr)

# BEGIN LAYOUT ANALYSIS
# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)

# loop over all pages in the document
for page in PDFPage.create_pages(document):

    # read the page into a layout object
    interpreter.process_page(page)
    layout = device.get_result()

    print(page.mediabox)

    # extract text from this object
    parse_obj(layout._objs,
              page.mediabox)

cv2.imwrite(output_path, m_image)