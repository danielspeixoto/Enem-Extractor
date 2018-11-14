from domain import filtering


def start(config):
    print("Import questions from repo")
    questions = config.repo.all()

    print("Filtering questions that we are able to process")
    questions, _ = filtering.pdf_questions(questions)

    # print("Uploading questions to Bucket")
    # print("Performing OCR")
    # print("Validating OCR results and its structures(5 alternatives)")

