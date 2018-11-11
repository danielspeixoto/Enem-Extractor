from pyPdf import PdfFileReader, PdfFileWriter

import pdf


class PDFQuestion:

    def __init__(self, lower, upper, page):
        self.lower = lower
        self.upper = upper
        self.page = page

    def save_as_pdf(self, pdf_input_path, output_path):
        with open(pdf_input_path, "rb") as pdf_file:
            pdf_input = PdfFileReader(pdf_file)
            output = PdfFileWriter()

            page = pdf_input.getPage(self.page)
            page = pdf.mod_page(page, lower=self.lower, upper=self.upper)
            output.addPage(page)

            with open(output_path, "wb") as out_f:
                output.write(out_f)
