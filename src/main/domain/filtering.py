def pdf_questions(questions):
    filtered = []
    excluded = []
    for question in questions:
        if _contain_image(question):
            excluded.append(question)
        else:
            filtered.append(question)
    return filtered, excluded

def _contain_image(question):
    pass