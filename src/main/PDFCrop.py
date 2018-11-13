import os
from pyPdf import PdfFileWriter, PdfFileReader
import pdf
import image
from Question import PDFQuestion

drop = 100


def find(pdf_input_path, pdf_page_path,
         working_dir, pattern_path):

    iteration = 0
    page_number = 0
    filename = "enem"
    working_dir = working_dir + "/" + str(iteration) + "/"
    if not os.path.exists(working_dir):
        os.mkdir(working_dir, 0755)
    img_path = working_dir + filename + ".jpg"
    ot_path = working_dir + filename + "-initial.pdf"

    questions = []
    question = PDFQuestion()

    i = 0

    pdf.crop(pdf_input_path, pdf_page_path)
    while True:
        i += 1
        while True:
            image.pdf2img(pdf_page_path, img_path)
            _, pattern_occurrence_y = image.find(pattern_path, img_path)
            _, img_height = image.size(img_path)
            if pattern_occurrence_y is not None:
                break
            else:
                # this question will be lost
                question = PDFQuestion()
                page_number += 1
                with open(pdf_input_path) as question_pdf_file:
                    enem_pdf = PdfFileReader(question_pdf_file)
                    if not page_number < enem_pdf.numPages:
                        return questions
                    with open(pdf_page_path, "wb") as page_file:
                        output = PdfFileWriter()
                        page = enem_pdf.getPage(page_number)
                        output.addPage(page)
                        output.write(page_file)
        with open(pdf_page_path) as page_file:
            print("Question " + str(i) + " at page " + str(page_number))
            page_pdf = PdfFileReader(page_file)
            page = page_pdf.getPage(0)
            lower, upper = get_coordinates(page,
                                           img_height,
                                           pattern_occurrence_y)
            question.upper = upper[0], lower[1]

            question = PDFQuestion()
            # We only append here because we dont want do add the first one
            questions.append(question)
            question.page = page_number
            question.lower = lower
            question.upper = page.mediaBox.getUpperRight_x(),\
                             page.mediaBox.getUpperRight_y()

            c_lower = lower[0], lower[1] - drop
            pdf.mod_page(page, lower=c_lower)
            output = PdfFileWriter()
            output.addPage(page)

            with open(ot_path, "wb") as ot_file:
                output.write(ot_file)
                aux = pdf_page_path
                pdf_page_path = ot_path
                ot_path = aux


def get_coordinates(page, img_height, point_y):
    pdf_height = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()

    pattern_pdf_y = int((pdf_height * point_y) / img_height)

    pattern_lower_coordinates = (page.mediaBox.getLowerLeft_x(),
                                 page.mediaBox.getUpperRight_y() + pattern_pdf_y)
    pattern_upper_coordinates = page.mediaBox.upperRight
    return pattern_lower_coordinates, pattern_upper_coordinates


def crop(input_path, output_path, page_number):
    with open(input_path, "rb") as pdf_file:
        pdf_input = PdfFileReader(pdf_file)
        page = pdf_input.getPage(page_number)
        pdf.crop(input_path, output_path,
                 lower=(page.mediaBox.getLowerLeft_x(),
                        page.mediaBox.getLowerLeft_y() - drop))
