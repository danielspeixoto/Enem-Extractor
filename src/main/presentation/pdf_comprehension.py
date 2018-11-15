from domain import filtering


def start(config):
    print("Import questions from repo")
    questions = config.repo.all()

    print("Filtering questions that we are able to process")
    questions, _ = filtering.pdf_questions(questions, config.working_pdf, config.working_dir + "/filtering/")

    # print("Uploading questions to Bucket")
    # print("Performing OCR")
    # print("Validating OCR results and its structures(5 alternatives)")

