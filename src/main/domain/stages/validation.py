class Validator:

    def __init__(self, amount_of_questions):
        self.amount_of_questions = amount_of_questions
        pass

    def validate(self, questions):
        is_ok = True
        if len(questions) != self.amount_of_questions:
            is_ok = False
            print("Different number of questions")
            print("Expected %s, Got %s",
                  self.amount_of_questions, len(questions))
        return is_ok