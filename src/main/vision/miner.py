output_path = "data/contoured.jpg"
img_path = "data/out.jpg"

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
import image

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
    # loop over the object list
    for obj in lt_objs:

        if isinstance(obj, pdfminer.layout.LTAnno) or isinstance(obj, pdfminer.layout.LTChar):
            continue

        color = (255, 255, 0)
        ww = 5
        if False:
            pass
        elif isinstance(obj, pdfminer.layout.LTFigure):
            color = (0, 255, 0)
        # elif isinstance(obj, pdfminer.layout.LTImage):
        #     color = (255, 0, 0)
        # elif isinstance(obj, pdfminer.layout.LTCurve):
        #     color = (0, 0, 255)
        # elif isinstance(obj, pdfminer.layout.LTTextLine):
        #     color = (255, 0, 255)
        else:
            ww = 5
            print(obj)

        y = int(convert_y(obj.bbox[1], hei))
        x = int(convert(obj.bbox[0], hei))
        w = int(convert(obj.width, hei))
        h = int(convert(obj.height, hei))

        cv2.rectangle(m_image, (x, y), (x + w, y - h), color, ww)

        if isinstance(obj, pdfminer.layout.LTContainer):
            parse_obj(obj._objs, mediabox)

# Open a PDF file.
fp = open('data/out.pdf', 'rb')

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
