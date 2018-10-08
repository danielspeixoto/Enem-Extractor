from copy import copy

from pyPdf import PdfFileWriter, PdfFileReader
import pdf
import image


pdf.crop("/home/daniel/Documents/enem/2017-1.pdf", "data/out.pdf", (311, 730 - 100), (59, 60))
print "ENEM borders cut out"

image.pdf2img("data/out.pdf", "data/out.jpg")
print "PDF transformed to a image"

cc = image.find("res/question_pattern.png", "data/out.jpg")
print "%s separator(s) found" % str(len(cc))
print(cc)

image_x, image_y = image.size("data/out.jpg")
separator = 0
for c in cc:
    separator = separator + 1
    separator_y = c[1]
    with open("data/out.pdf", "rb") as f:
        input1 = PdfFileReader(f)
        output = PdfFileWriter()

        numPages = input1.getNumPages()

        # excluded = [0, numPages - 1]
        for page_index in range(numPages):
            page = copy(input1.getPage(page_index))
            pdf_y = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()
            coord_y = pdf_y - int((pdf_y * separator_y) / image_y)
            coords = (page.mediaBox.getLowerLeft_x(), page.mediaBox.getLowerLeft_y() - coord_y + 5)
            page = pdf.mod_page(page, coords, page.mediaBox.upperRight)
            output.addPage(page)

        with open("data/" + str(separator) + ".pdf", "wb") as out_f:
            output.write(out_f)
            print "Question %s saved" % separator

        output = PdfFileWriter()

        for page_index in range(numPages):
            page = copy(input1.getPage(page_index))
            pdf_y = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()
            print pdf_y
            coord_y = int((pdf_y * separator_y) / image_y)
            print(coord_y)
            coords = (page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y() + coord_y + 5)
            n = (page.mediaBox.getLowerLeft_x(), page.mediaBox.getLowerLeft_y() + 100)
            page = pdf.mod_page(page, n, coords)
            output.addPage(page)

        with open("data/others.pdf", "wb") as out_f:
            output.write(out_f)
    break

