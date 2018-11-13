import os
from pyPdf import PdfFileWriter, PdfFileReader
import pdf
import image
from PDFParts import PDFPortion
from Question import Question


def find(pdf_input_path, working_dir, pattern_path, end_pattern_path):
    filename = "enem"
    img_path = working_dir + filename + ".jpg"

    current_pdf_path = working_dir + filename + "-aux0.pdf"
    aux_pdf_path = working_dir + filename + "-aux1.pdf"

    questions = []

    question_number = 0

    # Copies original PDF
    pdf.crop(pdf_input_path, current_pdf_path)

    with open(pdf_input_path) as question_pdf_file:
        enem_pdf = PdfFileReader(question_pdf_file)
        num_of_pages = enem_pdf.numPages
        first_page = enem_pdf.getPage(0)
        pdf_height = first_page.mediaBox.getLowerLeft_y() - first_page.mediaBox.getUpperRight_y()

    for page_number in range(num_of_pages):
        print("Page " + str(page_number))
        _copy_page(pdf_input_path, current_pdf_path, page_number)

        coordinates = _get_coordinates(current_pdf_path,
                                       img_path,
                                       pattern_path)
        pdf_portion = PDFPortion()
        pdf_portion.page = page_number
        is_page_start = True
        while coordinates is not None:
            lower, upper = coordinates
            # A question end is where a separator is found
            pdf_portion.upper = upper[0], lower[1]

            # If last portion was part of a already existing question
            # adds it to last inserted question
            if is_page_start:
                # It is allowed 30 units of distance from start
                # to not be considered another question
                # This is also used to skip section start statements
                # Ex.: Mathematics and Physics questions from x to y...
                if lower[1] < pdf_height - 30:
                    print("|---- Question " + str(question_number) + ".2")
                    questions[-1].add_part(pdf_portion)

            question_number += 1
            print("|---- Question " + str(question_number) + ".1")
            question = Question()
            pdf_portion = PDFPortion()
            pdf_portion.page = page_number
            question.add_part(pdf_portion)
            questions.append(question)
            # Another question start is where a separator is found
            pdf_portion.lower = lower
            with open(current_pdf_path) as page_file:
                page_pdf = PdfFileReader(page_file)
                page = page_pdf.getPage(0)

                pdf_portion.upper = page.mediaBox.getUpperRight_x(), \
                                    page.mediaBox.getUpperRight_y()

                # Crops below pattern
                aux_lower = lower[0], lower[1] - 100
                pdf.mod_page(page, lower=aux_lower)
                output = PdfFileWriter()
                output.addPage(page)
                with open(aux_pdf_path, "wb") as aux_pdf_file:
                    output.write(aux_pdf_file)
                    current_pdf_path, aux_pdf_path = aux_pdf_path, current_pdf_path

            coordinates = _get_coordinates(current_pdf_path,
                                           img_path,
                                           pattern_path)
            is_page_start = False
    return questions


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

def _copy_page(pdf_input_path, pdf_output, page_number):
    with open(pdf_input_path) as question_pdf_file:
        enem_pdf = PdfFileReader(question_pdf_file)
        page = enem_pdf.getPage(page_number)
        with open(pdf_output, "wb") as page_file:
            output = PdfFileWriter()
            output.addPage(page)
            output.write(page_file)
