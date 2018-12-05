# coding=utf-8
import pandas as pd

def domain_number(year, day, question_idx):
    if year >= 2017:
        if day == 2:
            if question_idx < 45:
                return "naturais", question_idx
            else:
                return "matematica", question_idx
        else:
            if question_idx < 5:
                return "ingles", question_idx
            elif question_idx < 10:
                return "espanhol", question_idx - 5
            elif question_idx < 50:
                return "linguagens", question_idx - 5
            else:
                return "humanas", question_idx - 5
    else:
        if day == 2:
            if question_idx < 45:
                return "humanas", question_idx
            else:
                return "naturais", question_idx
        else:
            if question_idx < 5:
                return "ingles", question_idx
            elif question_idx < 10:
                return "espanhol", question_idx - 5
            elif question_idx < 50:
                return "linguagens", question_idx - 5
            else:
                return "matematica", question_idx - 5

def answer(question_idx, micro_path, color, day, year):
    if day == 2:
        question_idx += 90
        if year >= 2017:
            # First day had 95 questions instead of only 90
            question_idx += 5
    df = pd.read_csv(micro_path, sep=";")
    df = df.loc[df['TX_COR'] == color]
    ans = df.iloc[question_idx, 3]
    return ord(ans[0]) - ord('A')