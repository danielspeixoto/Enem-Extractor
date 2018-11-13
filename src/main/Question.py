import os


class Question:

    def __init__(self):
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)

    def save_as_pdf(self, pdf_input_path, output_path):
        i = 0
        if not os.path.exists(output_path):
            os.mkdir(output_path, 0755)
        for part in self.parts:
            part.save_as_pdf(pdf_input_path, output_path + "/" +
                             str(i) + ".pdf")
            i += 1