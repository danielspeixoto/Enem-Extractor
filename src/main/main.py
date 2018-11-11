import pdf

from PDFCrop import find

from Question import PDFQuestion

res_folder = "/home/daniel/PycharmProjects/enem-parser/res/"
data_folder = "/home/daniel/PycharmProjects/enem-parser/data/"
enem_path = "/home/daniel/Documents/enem/2017-1.pdf"
question_folder = "/home/daniel/PycharmProjects/enem-parser/questions/"

page_index = 2

pdf.crop(enem_path,
         data_folder + "out.pdf",
         (311, 730), (55, 60), pages=[page_index])

print "ENEM borders cut out"

lower, upper = find(data_folder + "/out.pdf",
                    data_folder + "/others.pdf",
                    data_folder,
                    res_folder + "/question_pattern.png")

q = PDFQuestion(lower, upper, page_index)

q.save_as_pdf(enem_path,
              question_folder + "/1.pdf")
