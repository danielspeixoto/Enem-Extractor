from domain.tagger import domain_number


def format_save(config):
    questions = config.repo.all()
    i = 0
    for question in questions:
        i += 1
        tags = [domain_number(config.metadata.year, config.metadata.day, i),
                str(config.metadata.year), "enem"]
        question.save_as_pdf(config.working_pdf, config.question_folder + str(i))