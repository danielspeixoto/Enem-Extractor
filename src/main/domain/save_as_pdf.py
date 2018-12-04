def questions(questions, input, output_folder):
    i = 0
    for question in questions:
        i += 1
        question.save_as_pdf(input, output_folder + str(i))