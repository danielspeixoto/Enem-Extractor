from domain.tagger import domain_number, answer

import json

def format_save(config):
    questions = config.repo.all()
    i = 0
    for question in questions:
        i += 1
        current_folder = config.question_folder + "/" + str(i) + "/"
        domain, number = domain_number(config.metadata["year"], config.metadata["day"], i)
        meta = {
            "year": str(config.metadata["year"]),
            "source": "enem",
            "tags": domain,
            "number": str(number),
            "answer": answer(i - 1, config.microdata_path,
                             config.metadata["color"], config.metadata["day"],
                             config.metadata["year"])
        }
        question.save_as_pdf(config.working_pdf, current_folder)
        with open(current_folder + 'meta.json', 'w') as fp:
            json.dump(meta, fp)
        print(str(i) + " exported")
