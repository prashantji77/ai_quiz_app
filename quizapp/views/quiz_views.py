from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from quizapp.models import *
import json, requests
from django.shortcuts import redirect,render,get_object_or_404
import re
from quizapp.utils.ai_client import OpenRouterClient
from quizapp.services.quiz_services import create_quiz_session
from quizapp.constraints.constants import ERROR_MESSAGES
from quizapp.forms import AnswerForm

@login_required
def save_quiz(request):
    if request.method == 'POST':
        user=request.user
        class_choice = request.POST.get('class_choice')
        subject = request.POST.get('subject')
        topic = request.POST.get('topic')
        difficulty = request.POST.get('difficulty')
        number_of_questions = request.POST.get('num_questions')
        # print(class_choice, subject, topic, difficulty, number_of_questions)

        # Require class_choice OR other fields
        if not class_choice or not subject or not topic or not difficulty or not number_of_questions:
            messages.error(request, "Please fill in all fields. Provide either a Class or a Job Field.")
            return render(request, 'quiz/maths-quiz.html')
        else:
            try:
                number_of_questions = int(number_of_questions)
                if number_of_questions <= 0 or number_of_questions > 20:
                    messages.error(request, "Number of questions must be between 1 and 20.")
                    return render(request, 'quiz/maths-quiz.html')
            except ValueError:
                messages.error(request, "Invalid number of questions.")
                return render(request, 'quiz/maths-quiz.html')

        client =OpenRouterClient()
        
        prompt=f"""Generate {number_of_questions} Multiple Choice Questions.
 
                        Class: {class_choice if class_choice else "N/A"}
                        Subject: {subject if subject else "N/A"}
                        Topic: {topic}
                        Difficulty: {difficulty}

                        Each question must:
                        1. Be relevant to the given subject/topic.
                        2. Match the specified difficulty level.

                        Use this EXACT format for each question:

                        **Question X**
                        [Question text]
                        A) [Option A]
                        B) [Option B]
                        C) [Option C]
                        D) [Option D]

                        **Answer: [Correct Letter]) [Full correct answer text]**

                        Example:
                        **Question 1**
                        What is the basic unit of life?
                        A) Tissue
                        B) Cell
                        C) Organ
                        D) Organ system

                        **Answer: B) Cell**

                        Now generate questions following this exact pattern:"""

        try:
            ai_content = client.call_ai(prompt)
            # print("-------------------------------------------------------")
            # print(f"AI Content: {ai_content}")
            session = create_quiz_session(user=request.user, class_choice=class_choice, difficulty=difficulty, topic=topic, subject=subject, ai_content=ai_content)

            first_new_question = session.questions.order_by('id').first()
            return redirect('quiz', question_id=first_new_question.id)
            

        except Exception:
            return render(request, "quiz/maths-quiz.html", {"error": ERROR_MESSAGES["api_failed"]})
        
    else:
        return render(request, 'quiz/maths-quiz.html')





@login_required
def quiz_view(request, question_id):
    user = request.user
    question = get_object_or_404(Question, user=user, id=question_id)
    form = AnswerForm(question, request.POST or None)

    # Determine the next question within the same session only
    next_question = Question.objects.filter(user=user, session=question.session, id__gt=question.id).order_by('id').first()
    next_question_id = next_question.id if next_question else None

   
    session_questions_qs = Question.objects.filter(user=user, session=question.session).order_by('id')
    total_questions = session_questions_qs.count()
    session_questions = list(session_questions_qs)
    try:
        current_index = session_questions.index(question) + 1
    except ValueError:
        current_index = 1
    progress_percent = int((current_index / total_questions) * 100) if total_questions else 0
    existing_result = Result.objects.filter(user=user, session=question.session, question=question).first()

    if request.method == "POST":
        if form.is_valid():
            user_choice = form.cleaned_data['option']
            is_correct = user_choice == question.correct_answer

            # Persist the user's answer
            options_list = [opt.text for opt in question.options.all()]
            Result.objects.update_or_create(
                user=user,
                session=question.session,
                question=question,
                defaults={
                    'selected_option': user_choice,
                    'correct_answer_snapshot': question.correct_answer,
                    'options_snapshot': options_list,
                    'is_correct': is_correct,
                }
            )

            if next_question_id:
                return redirect('quiz', question_id=next_question_id)
            # If this was the LAST question, redirect to the finish view.
            else:
                return redirect('finish_quiz') # CHANGED

    return render(request, "quiz/quiz.html", {
        "question": question,
        "form": form,
        "next_question_id": next_question_id,
        "current_index": current_index,
        "total_questions": total_questions,
        "progress_percent": progress_percent,
        "existing_result": existing_result,
    })


@login_required
def finish_quiz(request):
    """
    Finish the quiz: Mark the session as inactive, calculate final score,
    and redirect to results. Handles both POST from a form and GET from a redirect.
    """
    user = request.user
    
    # Find the user's currently active quiz session
    latest_session = QuizSession.objects.filter(user=user, is_active=True).order_by('-created_at').first()

    if latest_session:
        # Mark the profile as no longer having an active quiz
        if user.profile.is_quiz_active:
            user.profile.is_quiz_active = False
            user.profile.save()

        # Calculate and persist the final score for the session
        session_results = Result.objects.filter(user=user, session=latest_session)
        
        # Use total created questions for accuracy
        total_questions = latest_session.questions.count()
        correct_answers = session_results.filter(is_correct=True).count()

        latest_session.total_questions = total_questions
        latest_session.score = correct_answers
        latest_session.is_active = False
        latest_session.save()
        
        # Redirect to the results page for this specific session
        return redirect('quiz_results_session', session_id=latest_session.id)

    # If no active session is found for some reason, redirect to the dashboard or home.
    messages.warning(request, "No active quiz session found to finish.")
    return redirect('maths-quiz') # Or your quiz home page