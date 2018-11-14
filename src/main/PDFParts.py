from pyPdf import PdfFileReader, PdfFileWriter

import pdf_utils


class PDFPortion:

    def __init__(self):
        self.lower = None
        self.upper = None
        self.page = None

    def save_as_pdf(self, pdf_input_path, output_path):
        with open(pdf_input_path, "rb") as pdf_file:
            pdf_input = PdfFileReader(pdf_file)
            output = PdfFileWriter()

            page = pdf_input.getPage(self.page)
            page = pdf_utils.mod_page(page, lower=self.lower, upper=self.upper)
            output.addPage(page)

            with open(output_path, "wb") as out_f:
                output.write(out_f)
