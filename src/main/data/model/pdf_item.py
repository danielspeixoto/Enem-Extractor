import os

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

from util.vision import pdf_utils


class Exam:

    def __init__(self):
        self.questions = []
        self.pdf_file = None

class Question:

    def __init__(self):
        self.parts = []
        self.number = None
        self.pdf_file = None

    def add_part(self, part):
        self.parts.append(part)

    def save_as_pdf(self, pdf_input_path, output_path):
        i = 0
        if not os.path.exists(output_path):
            os.mkdir(output_path, 0755)
        for part in self.parts:
            part.save_as_pdf(pdf_input_path,
                             output_path + "/" +
                             str(i) + ".pdf")
            i += 1

        merger = PdfFileMerger()
        for i in range(len(self.parts)):
            merger.append(
                PdfFileReader(
                    file(
                        output_path + "/" + str(i) + ".pdf", 'rb'
                    )
                )
            )
        merger.write(output_path + "/" + "question.pdf")
        for i in range(len(self.parts)):
            os.remove(
                output_path + "/" + str(i) + ".pdf"
            )



class Portion:

    def __init__(self):
        self.upper = None
        self.lower = None
        self.page = None

    def save_as_pdf(self, pdf_input_path, output_path):
        with open(pdf_input_path, "rb") as pdf_file:
            pdf_input = PdfFileReader(pdf_file)
            output = PdfFileWriter()

            page = pdf_input.getPage(self.page)
            page = pdf_utils.mod_page(page,
                                      upper=self.upper,
                                      lower=self.lower)
            output.addPage(page)

            with open(output_path, "wb") as out_f:
                output.write(out_f)

