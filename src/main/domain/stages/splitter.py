import os
from pyPdf import PdfFileWriter, PdfFileReader
import util.vision.pdf_utils
import util.vision.image
from data.model.pdf_item import Portion, Question
from util.vision import pdf_utils


def split_in_questions(pdf_input_path, working_dir, pattern_path):
    filename = "enem"
    img_path = working_dir + filename + ".jpg"

    current_pdf_path = working_dir + filename + "-aux0.pdf"
    aux_pdf_path = working_dir + filename + "-aux1.pdf"

    questions = []

    question_number = 0

    # Copies original PDF
    util.vision.pdf_utils.crop(pdf_input_path, current_pdf_path)

    with open(pdf_input_path) as question_pdf_file:
        enem_pdf = PdfFileReader(question_pdf_file)
        num_of_pages = enem_pdf.numPages
        first_page = enem_pdf.getPage(0)
        pdf_height = first_page.mediaBox.getUpperRight_y() - first_page.mediaBox.getLowerLeft_y()
        pdf_top = first_page.mediaBox.getUpperRight_y()
        pdt_bottom = first_page.mediaBox.getLowerLeft_y()

    for page_number in range(num_of_pages):
        print("Page " + str(page_number + 1))
        util.vision.pdf_utils.save_page(pdf_input_path, current_pdf_path, page_number)

        lower, upper = _get_coordinates(current_pdf_path,
                                        img_path,
                                        pattern_path)
        pdf_portion = Portion()
        pdf_portion.page = page_number
        # It is allowed 100 units of distance from start
        # to not be considered another question
        # This is also used to skip section start statements
        # Ex.: Mathematics and Physics questions from x to y...
        if upper is not None and upper[1] < pdf_top - 100:
            print("|---- Question " + str(question_number) + ".2")
            questions[-1].add_part(pdf_portion)
            _, pdf_portion.upper = get_dimensions(current_pdf_path)
        while upper is not None:
            # A question end is where a separator is found
            pdf_portion.lower = lower[0], upper[1]

            # If last portion was part of a already existing question
            # adds it to last inserted question

            question_number += 1
            print("|---- Question " + str(question_number) + ".1")
            question = Question()
            question.pdf_file = pdf_input_path
            question.number = question_number
            pdf_portion = Portion()
            pdf_portion.page = page_number
            question.add_part(pdf_portion)
            questions.append(question)
            # Another question start is where a separator is found
            pdf_portion.upper = upper

            page_lower, page_upper = get_dimensions(current_pdf_path)
            pdf_portion.lower = page_lower

            # Crops below pattern
            aux_upper = upper[0], upper[1] - 100

            pdf_utils.mod_save_page(current_pdf_path, aux_pdf_path, 0, upper=aux_upper)
            # Switches input pdf
            current_pdf_path, aux_pdf_path = aux_pdf_path, current_pdf_path

            lower, upper = _get_coordinates(current_pdf_path,
                                            img_path,
                                            pattern_path)
    os.remove(aux_pdf_path)
    os.remove(current_pdf_path)
    os.remove(img_path)
    return questions


def get_dimensions(pdf_path):
    with open(pdf_path) as page_file:
        page_pdf = PdfFileReader(page_file)
        page = page_pdf.getPage(0)
        lower = (page.mediaBox.getLowerLeft_x(),
                 page.mediaBox.getLowerLeft_y())
        upper = (page.mediaBox.getUpperRight_x(),
                 page.mediaBox.getUpperRight_y())
        return lower, upper


def _get_coordinates(pdf_page_path, img_path, pattern_path):
    util.vision.image.pdf2img(pdf_page_path, img_path)
    _, pattern_occurrence_y = util.vision.image.find(pattern_path, img_path)
    if pattern_occurrence_y is None:
        return None, None

    with open(pdf_page_path) as page_file:
        page_pdf = PdfFileReader(page_file)
        page = page_pdf.getPage(0)
        pdf_height = page.mediaBox.getUpperRight_y() - page.mediaBox.getLowerLeft_y()

    _, img_height = util.vision.image.size(img_path)
    # Returns the equivalent point at the specified PDF
    pattern_pdf_y = int((pdf_height * pattern_occurrence_y) / img_height)

    pattern_lower_coordinates = (page.mediaBox.getLowerLeft_x(),
                                 page.mediaBox.getLowerLeft_y())
    pattern_upper_coordinates = (page.mediaBox.getUpperRight_x(),
                                 page.mediaBox.getLowerLeft_y() + pattern_pdf_y)
    return pattern_lower_coordinates, pattern_upper_coordinates
