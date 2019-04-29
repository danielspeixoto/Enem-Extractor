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

        left_column_pdf_path = working_dir + "left.pdf"
        right_column_pdf_path = working_dir + "right.pdf"
        one_column_pdf_path = working_dir + "one.pdf"

        with open(input_path, "rb") as input_pdf:
            pdf_file = PdfFileReader(input_pdf)
            all_pages = range(pdf_file.numPages)

        top = 755
        low = 65
        start = 55
        middle = 320
        end = 585
        gap = 0

        if self.year >= 2016:
            top = 750
            low = 60
            start = 55
            middle = 310
            end = 570

        crop(input_path,
             left_column_pdf_path,
             (start, low), (middle, top),
             excluded=excluded_pages + one_column_pages)

        crop(input_path,
             right_column_pdf_path,
             (middle + gap, low), (end, top),
             excluded=excluded_pages + one_column_pages)

        crop(input_path,
             one_column_pdf_path,
             (start, low), (end, top), pages=one_column_pages)

        one_column_pages_idx = 0
        two_column_pages_idx = 0

        left_column_pdf = PdfFileReader(open(left_column_pdf_path, "rb"))
        right_column_pdf = PdfFileReader(open(right_column_pdf_path, "rb"))
        one_column_pdf = PdfFileReader(open(one_column_pdf_path, "rb"))
        output = PdfFileWriter()

        for page_index in all_pages:
            if page_index in excluded_pages:
                continue
            if page_index in one_column_pages:
                output.addPage(one_column_pdf.getPage(one_column_pages_idx))
                one_column_pages_idx += 1
            else:
                output.addPage(left_column_pdf.getPage(two_column_pages_idx))
                output.addPage(right_column_pdf.getPage(two_column_pages_idx))
                two_column_pages_idx += 1

        with open(output_path, "wb") as working_file:
            output.write(working_file)
        os.remove(left_column_pdf_path)
        os.remove(right_column_pdf_path)
        os.remove(one_column_pdf_path)
