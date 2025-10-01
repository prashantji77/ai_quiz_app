
def calculate_score(result_qs):
    total_questions= result_qs.count()
    score= result_qs.filter(is_correct=True).count()
    breakdown = [
        {
            "question_text" : r.question.text,
            "options" : r.options_snapshot,
            "selected" : r.selected_option,
            "correct" : r.correct_answer_snapshot,
            "is_correct" : r.is_correct,
        }
        for r in result_qs
    ]
    return score, total_questions, breakdown
