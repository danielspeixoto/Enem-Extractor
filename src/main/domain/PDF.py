from PyPDF2 import PdfFileWriter, PdfFileReader


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


def crop(input_path, output_path, lower=None, upper=None, pages=None, excluded=None):
    with open(input_path, "rb") as pdf:
        pdf_reader = PdfFileReader(pdf)

        pdf_output = PdfFileWriter()
        if pages is None:
            num_pages = pdf_reader.getNumPages()
            pages = range(num_pages)
        for i in pages:
            if excluded is not None and i in excluded:
                continue
            page = pdf_reader.getPage(i)
            mod_page(page, lower, upper)
            pdf_output.addPage(page)
        with open(output_path, "wb") as output_file:
            pdf_output.write(output_file)


def crop_page(page, output_path, lower=None, upper=None):
    pdf_output = PdfFileWriter()
    mod_page(page, lower, upper)

    with open(output_path, "wb") as output_file:
        pdf_output.write(output_file)


def save_page(pdf_input_path, pdf_output, page_number):
    with open(pdf_input_path) as question_pdf_file:
        enem_pdf = PdfFileReader(question_pdf_file)
        page = enem_pdf.getPage(page_number)
        with open(pdf_output, "wb") as page_file:
            output = PdfFileWriter()
            output.addPage(page)
            output.write(page_file)


def copy_page(pdf_input_path, pdf_output, page_number):
    with open(pdf_input_path) as question_pdf_file:
        enem_pdf = PdfFileReader(question_pdf_file)
        page = enem_pdf.getPage(page_number)
        with open(pdf_output, "a+") as page_file:
            output = PdfFileWriter()
            output.addPage(page)
            output.write(page_file)


def mod_save_page(pdf_input_path, pdf_output, page_number, lower=None, upper=None):
    with open(pdf_input_path) as question_pdf_file:
        enem_pdf = PdfFileReader(question_pdf_file)
        page = enem_pdf.getPage(page_number)
        mod_page(page, lower, upper)
        with open(pdf_output, "wb") as page_file:
            output = PdfFileWriter()
            output.addPage(page)
            output.write(page_file)
