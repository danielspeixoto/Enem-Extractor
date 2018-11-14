from PDFCrop import split_in_questions, save_questions_pdf
from PreProcessing import PreProcessing
from Validation import Validation

# Env Variable
enem_path = "/home/daniel/Documents/enem/2017-1.pdf"
question_folder = "/home/daniel/PycharmProjects/enem-parser/questions/"

amount_of_questions = 95
one_column_pages = [17, 25]
excluded_pages = [
    # Front page
    0,
    # Dissertation instructions
    18,
    # Dissertation
    31
]
# END of env variables

res_folder = "/home/daniel/PycharmProjects/enem-parser/res/"
data_folder = "/home/daniel/PycharmProjects/enem-parser/data/"
working_pdf = data_folder + "working.pdf"

print("Started")
preprocessing = PreProcessing(data_folder, enem_path,
                              working_pdf, one_column_pages,
                              excluded_pages)
preprocessing.linear_pdf()
print "ENEM is linear"

print("Splitting in questions")
questions = split_in_questions(working_pdf,
                               data_folder,
                               res_folder + "/question_pattern.png")
print("All questions retrieved")

print("Saving questions as PDF")
save_questions_pdf(questions, working_pdf, question_folder)

print("Validating results")
validation = Validation(amount_of_questions)
is_validated = validation.validate(questions)
if not is_validated:
    print("Data inconsistency, check results")
    exit(1)

# print("Filtering questions that we are able to process")

# Performing OCR
# Validating OCR results and its structures(5 alternatives)


