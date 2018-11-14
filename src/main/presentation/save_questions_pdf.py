def save_questions_pdf(config):
    questions = config.repo.all()
    i = 0
    for question in questions:
        i += 1
        question.save_as_pdf(config.working_pdf, config.question_folder + str(i))