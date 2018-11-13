from pyPdf import PdfFileReader, PdfFileWriter

import pdf

from PDFCrop import find

from PDFParts import PDFPortion

res_folder = "/home/daniel/PycharmProjects/enem-parser/res/"
data_folder = "/home/daniel/PycharmProjects/enem-parser/data/"
enem_path = "/home/daniel/Documents/enem/2017-1.pdf"
question_folder = "/home/daniel/PycharmProjects/enem-parser/questions/"

page_index = [1, 2, 3]

pdf.crop(enem_path,
         data_folder + "left.pdf",
         (310, 730), (55, 60), pages=page_index)

pdf.crop(enem_path,
         data_folder + "right.pdf",
         (570, 735), (315, 60), pages=page_index)

with open(data_folder + "/left.pdf") as l:
    left_pdf = PdfFileReader(l)
    with open(data_folder + "/right.pdf") as r:
        right_pdf = PdfFileReader(r)

        output = PdfFileWriter()
        page = 0
        pdfs = 2
        while pdfs > 0:
            if left_pdf.numPages > page:
                output.addPage(left_pdf.getPage(page))
            else:
                pdfs -= 1
            if right_pdf.numPages > page:
                output.addPage(right_pdf.getPage(page))
            else:
                pdfs -= 1
            page += 1
        with open(data_folder + "final.pdf", "wb") as f:
            output.write(f)
print "ENEM borders cut out"

qs = find(data_folder + "/final.pdf",
                    data_folder,
                    res_folder + "/question_pattern.png")
i = 0
for q in qs:
    i += 1
    q.save_as_pdf(data_folder + "final.pdf", question_folder + str(i) + ".pdf")

# q = PDFQuestion(lower, upper, page_index)
#
# q.save_as_pdf(enem_path,
#               question_folder + "/1.pdf")
