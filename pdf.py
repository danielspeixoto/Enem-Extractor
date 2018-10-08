from copy import copy

from pyPdf import PdfFileWriter, PdfFileReader


def mod_page(crop_page, lower, upper):
    new_page = copy(crop_page)
    new_page.mediaBox.upperRight = upper
    new_page.mediaBox.lowerLeft = lower
    new_page.cropBox.upperRight = upper
    new_page.cropBox.lowerLeft = lower
    new_page.trimBox.upperRight = upper
    new_page.trimBox.lowerLeft = lower
    return new_page


def crop(input_path, output_path, lower, upper):
    with open(input_path, "rb") as pdf:
        pdf_reader = PdfFileReader(pdf)
        pdf_output = PdfFileWriter()

        numPages = pdf_reader.getNumPages()

        # excluded = [0, numPages - 1]
        # for i in range(numPages):
        #     if i in excluded:
        #         pass
        i = 8
        page = copy(pdf_reader.getPage(i))
        page = mod_page(page, lower, upper)
        pdf_output.addPage(page)

        with open(output_path, "wb") as output_file:
            pdf_output.write(output_file)
