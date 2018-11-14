from PDFCrop import split_in_questions
from PreProcessing import PreProcessing

res_folder = "/home/daniel/PycharmProjects/enem-parser/res/"
data_folder = "/home/daniel/PycharmProjects/enem-parser/data/"
enem_path = "/home/daniel/Documents/enem/2017-1.pdf"
question_folder = "/home/daniel/PycharmProjects/enem-parser/questions/"
working_pdf = data_folder + "working.pdf"

one_column_pages = [17, 25]
excluded_pages = [
    # Front page
    0,
    # Dissertation instructions
    18,
    # Dissertation
    31
]

preprocessing = PreProcessing(data_folder, enem_path,
                              working_pdf, one_column_pages,
                              excluded_pages)
preprocessing.linear_pdf()

# questions = split_in_questions(working_pdf,
#                                data_folder,
#                                res_folder + "/question_pattern.png")
#
# print(len(questions))



#
# i = 0
# for question in questions:
#     i += 1
#     question.save_as_pdf(working_pdf, question_folder + str(i))
