from domain.stages import splitter
from domain.stages import pre_processing
from domain.stages import validation

# Returns questions found and bool that indicates error
def start(environment):
    preprocessing = pre_processing.PreProcessor(
        environment.working_dir, environment.enem_path,
        environment.working_pdf, environment.one_column_pages,
        environment.excluded_pages)
    preprocessing.linear_pdf()
    print "ENEM is linear"

    print("Splitting in questions")
    questions = splitter.split_in_questions(
        environment.working_pdf,
        environment.working_dir,
        environment.question_pattern)
    print("All questions retrieved")

    print("Validating results")
    validator = validation.Validator(environment.amount_of_questions)
    is_validated = validator.validate(questions)

    environment.repo.save(questions)

    if not is_validated:
        print("Data inconsistency, check results")
        return questions, True
    return questions, False