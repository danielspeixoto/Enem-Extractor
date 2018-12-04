# coding=utf-8
def domain_number(year, day, question_idx):
    if day == 2:
        if question_idx < 45:
            return "naturais", question_idx
        else:
            return "matemática", question_idx
    else:
        if question_idx < 5:
            return "inglês", question_idx
        elif question_idx < 10:
            return "espanhol", question_idx - 5
        elif question_idx < 50:
            return "linguagens", question_idx - 5
        else:
            return "matemática", question_idx - 5