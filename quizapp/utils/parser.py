import re
from quizapp.models import Question
from quizapp.constraints.constants import QUESTION_PATTERN

def parse_ai_response(content):
    matches=QUESTION_PATTERN.finditer(content)
    print(matches)
    questions=[]
    print(questions)
    for match in matches:
        question_text = match.group(1).strip()
        option_a = match.group(2).strip()
        option_b = match.group(3).strip()
        option_c = match.group(4).strip()
        option_d = match.group(5).strip()
        correct_answer= match.group(6).strip()

        all_options = [option_a, option_b, option_c, option_d]

        if question_text and all(all_options) and correct_answer:
            questions.append({
                "question":question_text,
                "options":all_options,
                "answer":correct_answer,
            })
    return questions

