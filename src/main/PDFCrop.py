import os
from pyPdf import PdfFileWriter, PdfFileReader
import pdf
import image
from PDFParts import PDFPortion

drop = 100


def find(pdf_input_path, pdf_page_path,
         working_dir, pattern_path):
    page_number = 0
    filename = "enem"
    img_path = working_dir + filename + ".jpg"
    aux_pdf_path = working_dir + filename + "-aux.pdf"

    questions = []
    pdf_portion = PDFPortion()

    question_number = 0

    # Copies original PDF
    pdf.crop(pdf_input_path, pdf_page_path)
    print("Page " + str(page_number))
    while True:
        coordinates = _get_coordinates(pdf_page_path,
                                       img_path,
                                       pattern_path)
        if coordinates is None:
            pdf_portion = PDFPortion()
            page_number += 1
            with open(pdf_input_path) as question_pdf_file:
                enem_pdf = PdfFileReader(question_pdf_file)
                if not page_number < enem_pdf.numPages:
                    # EOF
                    return questions
                page = enem_pdf.getPage(page_number)
                print("Page " + str(page_number))
                _copy_page_to(page, pdf_page_path)
            continue

        lower, upper = coordinates
        question_number += 1
        print("|---- Question " + str(question_number))
        # A question end is where a separator is found
        pdf_portion.upper = upper[0], lower[1]

        pdf_portion = PDFPortion()
        # We only append here because we don't want do add the first one
        questions.append(pdf_portion)
        # Another question start is where a separator is found
        pdf_portion.page = page_number
        pdf_portion.lower = lower
        with open(pdf_page_path) as page_file:
            page_pdf = PdfFileReader(page_file)
            page = page_pdf.getPage(0)

            pdf_portion.upper = page.mediaBox.getUpperRight_x(), \
                             page.mediaBox.getUpperRight_y()

            # Crops below pattern
            aux_lower = lower[0], lower[1] - drop
            pdf.mod_page(page, lower=aux_lower)
            output = PdfFileWriter()
            output.addPage(page)
            with open(aux_pdf_path, "wb") as aux_pdf_file:
                output.write(aux_pdf_file)
                pdf_page_path, aux_pdf_path = aux_pdf_path, pdf_page_path


def _get_coordinates(pdf_page_path, img_path, pattern_path):
    image.pdf2img(pdf_page_path, img_path)
    _, pattern_occurrence_y = image.find(pattern_path, img_path)
    if pattern_occurrence_y is None:
        return None

    with open(pdf_page_path) as page_file:
        page_pdf = PdfFileReader(page_file)
        page = page_pdf.getPage(0)
        pdf_height = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()

    _, img_height = image.size(img_path)
    # Returns the equivalent point at the specified PDF
    pattern_pdf_y = int((pdf_height * pattern_occurrence_y) / img_height)

    pattern_lower_coordinates = (page.mediaBox.getLowerLeft_x(),
                                 page.mediaBox.getUpperRight_y() + pattern_pdf_y)
    pattern_upper_coordinates = page.mediaBox.upperRight
    return pattern_lower_coordinates, pattern_upper_coordinates

def _copy_page_to(page, pdf_output):
    with open(pdf_output, "wb") as page_file:
        output = PdfFileWriter()
        output.addPage(page)
        output.write(page_file)
