from quizapp.models import QuizSession,Question,Option
from quizapp.utils.parser import parse_ai_response

def create_quiz_session(user, subject, topic, difficulty, ai_content, class_choice=None):
    session_title = f"{subject or 'Quiz'} - {topic} ({difficulty})"
    session = QuizSession.objects.create(user=user, title=session_title, is_active=True)
    # print(f"Creating quiz session: {session_title} for user: {user.username}")
    # print(f"AI Content: {ai_content}")
    if not ai_content:
        return session  # No AI content to parse, return empty session
    parsed_questions = parse_ai_response(ai_content)
    # print("-------------------------------------------------------")
    # print(f"Parsed Questions: {parsed_questions}")

    if not parsed_questions:
        return session  # No valid questions parsed, return empty session

    for q in parsed_questions:
        question_obj = Question.objects.create(
            user=user,
            session=session,
            text=q['question'],
            correct_answer=q['answer']
        )

        for opt in q['options']:
            Option.objects.create(user=user, question=question_obj,text=opt)
            
    return session


