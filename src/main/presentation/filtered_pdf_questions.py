from domain import filtering


def start(config):
    print("Import questions from repo")
    questions = config.repo.all()

    print("Filtering questions that we are able to process")
    questions, excluded = filtering.pdf_questions(questions, config.working_pdf, config.working_dir + "/filtering/")

    if len(excluded) == 0:
        print("All questions were accepted")
    else:
        question_numbers = ""
        for question in excluded:
            question_numbers += str(question.number) + " "
        print("Excluded questions: %s" % question_numbers)
        percent = len(excluded)/float(len(questions) + len(excluded))
        print("This represents %.2f of the total number of questions", percent)