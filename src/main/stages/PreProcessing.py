import os

from pyPdf import PdfFileReader, PdfFileWriter
import vision.pdf_utils


class PreProcessing:

    def __init__(self, working_dir, input_path, output_path,
                 one_column_pages, excluded_pages):
        self.working_pdf = output_path
        self.input_path = input_path
        self.left_column_pdf = working_dir + "left.pdf"
        self.right_column_pdf = working_dir + "right.pdf"
        self.one_column_pdf = working_dir + "one.pdf"
        self.one_column_pages = one_column_pages
        self.excluded_pages = excluded_pages

    def _copy_page(self, pdf_path, page_number, output):
        with open(pdf_path) as pdf_file:
            pdf_file = PdfFileReader(pdf_file)
            page = pdf_file.getPage(page_number)
            output.addPage(page)
            with open(self.working_pdf, "a") as working_file:
                output.write(working_file)

    def linear_pdf(self):
        with open(self.input_path) as input_pdf:
            pdf_file = PdfFileReader(input_pdf)
            all_pages = range(pdf_file.numPages)

        vision.pdf_utils.crop(self.input_path,
                                       self.left_column_pdf,
                                       (310, 735), (55, 60),
                                       excluded=self.excluded_pages + self.one_column_pages)

        vision.pdf_utils.crop(self.input_path,
                                       self.right_column_pdf,
                                       (570, 735), (315, 60),
                                       excluded=self.excluded_pages + self.one_column_pages)

        vision.pdf_utils.crop(self.input_path,
                                       self.one_column_pdf,
                                       (570, 735), (55, 60), pages=self.one_column_pages)

        one_column_pages = 0
        two_column_pages = 0

        left_column_pdf = PdfFileReader(file(self.left_column_pdf, "rb"))
        right_column_pdf = PdfFileReader(file(self.right_column_pdf, "rb"))
        one_column_pdf = PdfFileReader(file(self.one_column_pdf, "rb"))
        output = PdfFileWriter()
        for page_index in all_pages:
            if page_index in self.excluded_pages:
                continue
            if page_index in self.one_column_pages:
                output.addPage(one_column_pdf.getPage(one_column_pages))
                one_column_pages += 1
            else:
                output.addPage(left_column_pdf.getPage(two_column_pages))
                output.addPage(right_column_pdf.getPage(two_column_pages))
                two_column_pages += 1

        with open(self.working_pdf, "wb") as working_file:
            output.write(working_file)
        os.remove(self.left_column_pdf)
        os.remove(self.right_column_pdf)
        os.remove(self.one_column_pdf)
