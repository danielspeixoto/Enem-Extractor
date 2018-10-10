from copy import copy

import image
from pyPdf import PdfFileWriter, PdfFileReader
import pdf


def answers(working_dir, pattern_path, questions):
    for question in questions:
        question = str(question)
        question_path = working_dir + "/" + question
        content_path = question_path + "-content.pdf"
        question_pdf_path = question_path + ".pdf"
        img_path = question_path + ".jpg"
        image.pdf2img(question_pdf_path, img_path)
        print "Question PDF transformed to a image"

        _, separator_y = image.find(pattern_path, img_path)
        _, image_y = image.size(img_path)

        with open(question_pdf_path, "rb") as pdf_file:
            pdf_input = PdfFileReader(pdf_file)
            output = PdfFileWriter()

            num_pages = pdf_input.getNumPages()

            for page_index in range(num_pages):
                page = copy(pdf_input.getPage(page_index))
                pdf_y = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()
                coord_y = pdf_y - int((pdf_y * separator_y) / image_y)
                coords = (page.mediaBox.getLowerLeft_x(), page.mediaBox.getLowerLeft_y() - coord_y)
                page = pdf.mod_page(page, lower=coords)
                output.addPage(page)

            with open(question_path + "-answer.pdf", "wb") as out_f:
                output.write(out_f)
                print "Question %s answer saved" % question

        with open(question_pdf_path, "rb") as pdf_file:
            pdf_input = PdfFileReader(pdf_file)
            output = PdfFileWriter()

            for page_index in range(num_pages):
                page = pdf_input.getPage(page_index)
                pdf_y = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()
                coord_y = int((pdf_y * separator_y) / image_y)
                coords = (page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y() + coord_y + 2)
                page = pdf.mod_page(page, upper=coords)
                output.addPage(page)

            with open(content_path, "wb") as out_f:
                output.write(out_f)