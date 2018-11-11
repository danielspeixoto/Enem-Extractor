import os
from copy import copy

from pyPdf import PdfFileWriter, PdfFileReader
import pdf
import image


drop = 100


def find(pdf_input_path, others_path, working_dir, pattern_path, page_number=0, iteration=0):
    filename = "enem"
    working_dir = working_dir + "/" + str(iteration) + "/"
    if not os.path.exists(working_dir):
        os.mkdir(working_dir, 0755)
    img_path = working_dir + filename + ".jpg"
    cropped_pdf_path = working_dir + filename + "-cropped.pdf"

    # Crops below pattern
    crop(pdf_input_path, cropped_pdf_path, page_number)

    pdf_img_reference = cropped_pdf_path

    # Image Created
    image.pdf2img(pdf_img_reference, img_path)

    _, pattern_occurrence_y = image.find(pattern_path, img_path)
    _, img_height = image.size(img_path)

    with open(pdf_img_reference, 'rb') as question_pdf_file:
        question_pdf = PdfFileReader(question_pdf_file)

        page = question_pdf.getPage(page_number)
        lower, upper = get_coordinates(page, img_height, pattern_occurrence_y)
        pdf.mod_page(page, lower=lower, upper=upper)
        output = PdfFileWriter()
        output.addPage(page)

        with open(others_path, "wb") as out_f:
            output.write(out_f)

    with open(pdf_img_reference, 'rb') as question_pdf_file:
        question_pdf = PdfFileReader(question_pdf_file)

        page = question_pdf.getPage(page_number)
        pdf_height = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()
        distance_point_y = int((pdf_height * pattern_occurrence_y) / img_height)
        upper = (page.mediaBox.getUpperRight_x(),
                 page.mediaBox.getUpperRight_y() + distance_point_y + 2)
        lower = (page.mediaBox.getLowerLeft_x(),
                 # We add 16 so we can crop out "Questao X"
                 page.mediaBox.getLowerLeft_y() + drop - 16)

        return lower, upper


def get_coordinates(page, img_height, point_y):
    pdf_height = page.mediaBox.getLowerLeft_y() - page.mediaBox.getUpperRight_y()
    pattern_pdf_y = pdf_height - int((pdf_height * point_y) / img_height)

    pattern_lower_coordinates = (page.mediaBox.getLowerLeft_x(),
                                 page.mediaBox.getLowerLeft_y() - pattern_pdf_y - 13)
    pattern_upper_coordinates = page.mediaBox.upperRight
    return pattern_lower_coordinates, pattern_upper_coordinates


def crop(input_path, output_path, page_number):
    with open(input_path, "rb") as pdf_file:
        pdf_input = PdfFileReader(pdf_file)
        page = pdf_input.getPage(page_number)
        pdf.crop(input_path, output_path,
                 lower=(page.mediaBox.getLowerLeft_x(),
                        page.mediaBox.getLowerLeft_y() - drop))
