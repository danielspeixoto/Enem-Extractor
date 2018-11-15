from data.model import configuration
from presentation import filtered_pdf_questions
from presentation.save_questions_pdf import save_questions_pdf

print("Started")
config = configuration.Environment()

# questions, has_error = split_questions.start(config)

print("Saving questions as PDF")
# save_questions_pdf(config)

filtered_pdf_questions.start(config)

# if has_error:
#     print("Execution finished, errors were detected")
#     exit(1)

# print("Converting pdf to a comprehensible format")
# structured_questions, has_error = pdf_comprehension.start(config)
#
# if has_error:
#     print("Execution finished, errors were detected")
#     exit(1)
#
# # Review process
#
