from pyPdf import PdfFileWriter, PdfFileReader


def mod_page(crop_page, lower, upper):
    crop_page.mediaBox.upperRight = upper
    crop_page.mediaBox.lowerLeft = lower
    crop_page.cropBox.upperRight = upper
    crop_page.cropBox.lowerLeft = lower
    crop_page.trimBox.upperRight = upper
    crop_page.trimBox.lowerLeft = lower
    return crop_page


with open("/home/daniel/Documents/enem/2017-1.pdf", "rb") as in_f:
    input1 = PdfFileReader(in_f)
    output = PdfFileWriter()

    numPages = input1.getNumPages()

    # excluded = [0, numPages - 1]
    # for i in range(numPages):
    #     if i in excluded:
    #         pass
    i = 3
    page = input1.getPage(i)
    # TODO: 730
    page = mod_page(page, (311, 730), (59, 60))
    # print page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y()

    output.addPage(page)

    with open("data/out.pdf", "wb") as out_f:
        output.write(out_f)

from pdf2image import convert_from_path
pages = convert_from_path('data/out.pdf', 500)

for page in pages:
    page.save('data/out.jpg', 'JPEG')


import cv2
import numpy as np

image = cv2.imread("data/out.jpg")
template = cv2.imread("res/pattern.png")
image_y, image_x, _ = image.shape
result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
occurence_y, occurence_x = np.unravel_index(result.argmax(), result.shape)

with open("data/out.pdf", "rb") as f:
    input1 = PdfFileReader(f)
    output = PdfFileWriter()

    numPages = input1.getNumPages()

    # excluded = [0, numPages - 1]
    for i in range(numPages):
        page = input1.getPage(i)
        print page.mediaBox
        print page.cropBox.upperRight, page.cropBox.lowerLeft
        pdf_x, pdf_y = (page.mediaBox.getUpperRight_x() - page.mediaBox.getLowerLeft_x()) * -1,\
                       (page.mediaBox.getUpperRight_y() - page.mediaBox.getLowerLeft_y()) * -1

        coord_x = (pdf_x * occurence_x) / image_x
        coord_y = (pdf_y * occurence_y) / image_y

        print "coord y: %s" % coord_y

        coords = (page.mediaBox.getLowerLeft_x(), page.mediaBox.getLowerLeft_y() - coord_y + 3)
        print("coords")
        print coords
        page = mod_page(page, coords, page.mediaBox.upperRight)
        output.addPage(page)

    with open("data/a.pdf", "wb") as out_f:
        output.write(out_f)
