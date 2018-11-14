from domain import filtering


def start(config):
    print("Import questions from repo")
    questions = config.repo.all()

    print("Filtering questions that we are able to process")
    questions, excluded = filtering.pdf_questions(questions)

    if len(excluded) == 0:
        print("All questions were accepted")
    else:
        question_numbers = ""
        for question in excluded:
            question_numbers += str(question.number) + " "
        print("Excluded questions: %s" % question_numbers)