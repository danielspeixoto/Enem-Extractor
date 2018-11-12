from copy import copy

from pyPdf import PdfFileWriter, PdfFileReader


def mod_page(crop_page, lower=None, upper=None):
    if lower is None:
        lower = crop_page.mediaBox.lowerLeft
    if upper is None:
        upper = crop_page.mediaBox.upperRight
    new_page = crop_page
    new_page.mediaBox.upperRight = upper
    new_page.mediaBox.lowerLeft = lower
    new_page.cropBox.upperRight = upper
    new_page.cropBox.lowerLeft = lower
    new_page.trimBox.upperRight = upper
    new_page.trimBox.lowerLeft = lower
    return new_page


def crop(input_path, output_path, lower=None, upper=None, pages=None):
    with open(input_path, "rb") as pdf:
        pdf_reader = PdfFileReader(pdf)

        num_pages = pdf_reader.getNumPages()

        # excluded = [0, numPages - 1]
        # for i in range(numPages):
        #     if i in excluded:
        #         pass
        pdf_output = PdfFileWriter()
        if pages is None:
            pages = range(num_pages)
        for i in pages:
            page = pdf_reader.getPage(i)
            mod_page(page, lower, upper)
            pdf_output.addPage(page)
        with open(output_path, "wb") as output_file:
            pdf_output.write(output_file)


def crop_page(page, output_path, lower=None, upper=None):
    pdf_output = PdfFileWriter()
    page = mod_page(page, lower, upper)

    with open(output_path, "wb") as output_file:
        pdf_output.write(output_file)
