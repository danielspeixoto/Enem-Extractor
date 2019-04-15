import os
from PyPDF2 import PdfFileReader, PdfFileWriter

from src.main.domain.PDF import crop


class ENEMPreProcessor:

    def linear(self,
               working_dir,
               input_path,
               output_path,
               one_column_pages,
               excluded_pages):

        left_column_pdf = working_dir + "left.pdf"
        right_column_pdf = working_dir + "right.pdf"
        one_column_pdf = working_dir + "one.pdf"

        with open(input_path) as input_pdf:
            pdf_file = PdfFileReader(input_pdf)
            all_pages = range(pdf_file.numPages)

        crop(input_path,
             left_column_pdf,
             (55, 60), (310, 750),
             excluded=excluded_pages + one_column_pages)

        crop(input_path,
             right_column_pdf,
             (315, 60), (570, 750),
             excluded=excluded_pages + one_column_pages)

        crop(input_path,
             one_column_pdf,
             (55, 60), (570, 750), pages=one_column_pages)

        one_column_pages = 0
        two_column_pages = 0

        left_column_pdf = PdfFileReader(open(left_column_pdf, "rb"))
        right_column_pdf = PdfFileReader(open(right_column_pdf, "rb"))
        one_column_pdf = PdfFileReader(open(one_column_pdf, "rb"))
        output = PdfFileWriter()

        for page_index in all_pages:
            if page_index in excluded_pages:
                continue
            if page_index in one_column_pages:
                output.addPage(one_column_pdf.getPage(one_column_pages))
                one_column_pages += 1
            else:
                output.addPage(left_column_pdf.getPage(two_column_pages))
                output.addPage(right_column_pdf.getPage(two_column_pages))
                two_column_pages += 1

        with open(output_path, "wb") as working_file:
            output.write(working_file)
        os.remove(left_column_pdf)
        os.remove(right_column_pdf)
        os.remove(one_column_pdf)
