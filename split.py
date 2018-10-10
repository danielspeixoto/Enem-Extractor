from copy import copy

from pyPdf import PdfFileWriter, PdfFileReader
import pdf
import image

drop = 100


def split(input_path, working_dir, pattern_path):
    cropped_path = working_dir + "/cropped.pdf"
    question_path = working_dir + "/"
    others_path = working_dir + "/others.pdf"
    # Crops below pattern
    # with open(input_path, "rb") as pdf_file:
    #     pdf_input = PdfFileReader(pdf_file)
    #     page = pdf_input.getPage(0)
    #     pdf.crop(input_path, cropped_path, lower=(page.mediaBox.getLowerLeft_x(), page.mediaBox.getLowerLeft_y() - drop))


    cropped_path = input_path

    question_path += "/"
    img_path = cropped_path.split(".")[0] + ".jpg"
    image.pdf2img(cropped_path, img_path)
    print "PDF transformed to a image"
    #
    # separators = 0
    # _, separator_y = image.find(pattern_path, img_path)
    # separators = separators + 1
    # image_x, image_y = image.size(img_path)
    # with open(cropped_path, "rb") as pdf_file:
    #     pdf_input = PdfFileReader(pdf_file)
    #     output = PdfFileWriter()
    #
    #     num_pages = pdf_input.getNumPages()
    #
    #     for page_index in range(num_pages):
    #         page = copy(pdf_input.getPage(page_index))
    #         pdf_y = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()
    #         coord_y = pdf_y - int((pdf_y * separator_y) / image_y)
    #         coords = (page.mediaBox.getLowerLeft_x(), page.mediaBox.getLowerLeft_y() - coord_y + 5)
    #         page = pdf.mod_page(page, lower=coords, upper=page.mediaBox.upperRight)
    #         output.addPage(page)
    #
    #     with open(others_path, "wb") as out_f:
    #         output.write(out_f)
    #
    # with open(cropped_path, "rb") as pdf_file:
    #     pdf_input = PdfFileReader(pdf_file)
    #     output = PdfFileWriter()
    #
    #     for page_index in range(num_pages):
    #         page = pdf_input.getPage(page_index)
    #         pdf_y = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()
    #         coord_y = int((pdf_y * separator_y) / image_y)
    #         coords = (page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y() + coord_y + 2)
    #         n = (page.mediaBox.getLowerLeft_x(), page.mediaBox.getLowerLeft_y() + drop)
    #         page = pdf.mod_page(page, lower=n, upper=coords)
    #         output.addPage(page)
    #
    #     with open(question_path + str(separators) + ".pdf", "wb") as out_f:
    #         output.write(out_f)
    #         print "Question %s saved" % separators
