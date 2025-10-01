import os
from django.contrib import messages
from .models import Question, Option
import requests
import json
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import QuizSession, Question, Option, UserAnswer
from dotenv import load_dotenv

load_dotenv()

def save_new_quiz(request):
    if request.method == 'POST':
        # Ensure the browser session has a session_key (creates a session if needed)
        if not request.session.session_key:
            # This will create and persist a session key for the visitor
            request.session.save()

        # Check if user has an active quiz in their session
        if 'active_quiz_session_id' in request.session:
            active_session_id = request.session['active_quiz_session_id']
            try:
                active_session = QuizSession.objects.get(id=active_session_id, is_active=True)
                messages.warning(request, "You have an unfinished quiz. Please complete it first!")
                first_question = active_session.questions.order_by('id').first()
                if first_question:
                    return redirect('new-quiz', question_id=first_question.id)
            except QuizSession.DoesNotExist:
                # Clear the session if no active quiz found
                if 'active_quiz_session_id' in request.session:
                    del request.session['active_quiz_session_id']

        # Get form data
        class_choice = (request.POST.get('class_choice') or '').strip()
        job_choice = (request.POST.get('job_choice') or '').strip()
        subject_type = (request.POST.get('subject') or '').strip()
        topic_type = (request.POST.get('topic') or '').strip()
        difficulty_level = (request.POST.get('difficulty') or '').strip()
        number_of_questions = (request.POST.get('num_questions') or '').strip()

        # Require either class_choice OR job_choice, plus other fields
        if not (class_choice or job_choice) or not subject_type or not topic_type or not difficulty_level or not number_of_questions:
            messages.error(request, "Please fill in all fields. Provide either a Class or a Job Field.")
            return render(request, 'quiz_nologin/basic-quiz.html')

        api_key =  os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return render(request, 'quiz_nologin/basic-quiz.html', {'error': "API key not configured."})
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": "meta-llama/llama-3-8b-instruct",
                    "messages": [{
                        "role": "user",
                        "content": f"""Generate {number_of_questions} Multiple Choice Questions.

                        Class: {class_choice if class_choice else "N/A"}
                        Subject: {subject_type if subject_type else "N/A"}
                        Topic: {topic_type}
                        Difficulty: {difficulty_level}

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
                    }],
                    "max_tokens": 1000,
                })
            )
            response.raise_for_status()
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            return render(request, 'quiz_nologin/basic-quiz.html', {'error': f"API request failed: {e}"})
        except (KeyError, IndexError):
            return render(request, 'quiz_nologin/basic-quiz.html', {'error': "Could not parse API response."})

        # Parse questions
        pattern = re.compile(
            r"\*\*Question \d+\*\*\s*(.*?)\s*A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*?)\s*\*\*Answer: ([A-D])\)\s*(.*?)\*\*",
            re.S
        )

        # Create a new quiz session using the browser session key
        session_title = f"{subject_type or 'Quiz'} - {topic_type} ({difficulty_level})"
        # Ensure session_key is set (session.save() above should guarantee this)
        session_key = request.session.session_key or ''
        quiz_session = QuizSession.objects.create(
            session_key=session_key,
            title=session_title,
            is_active=True
        )

        matches = pattern.finditer(content)
        questions_created = 0

        for match in matches:
            question_text = match.group(1).strip()
            option_a = match.group(2).strip()
            option_b = match.group(3).strip()
            option_c = match.group(4).strip()
            option_d = match.group(5).strip()
            correct_letter = match.group(6).strip()
            correct_answer_text = match.group(7).strip()

            if question_text and all([option_a, option_b, option_c, option_d]) and correct_letter:
                # Create question
                question_obj = Question.objects.create(
                    session=quiz_session,
                    text=question_text,
                    correct_answer=f"{correct_letter}) {correct_answer_text}"
                )
                
                # Create options
                Option.objects.create(question=question_obj, text=option_a, letter='A')
                Option.objects.create(question=question_obj, text=option_b, letter='B')
                Option.objects.create(question=question_obj, text=option_c, letter='C')
                Option.objects.create(question=question_obj, text=option_d, letter='D')
                
                questions_created += 1

        if questions_created > 0:
            # Store active quiz session ID in user's session
            request.session['active_quiz_session_id'] = quiz_session.id
            
            # Redirect to first question
            first_question = quiz_session.questions.order_by('id').first()
            return redirect('new-quiz', question_id=first_question.id)
        else:
            # Delete the session if no questions were created
            quiz_session.delete()
            return render(request, 'quiz_nologin/basic-quiz.html', {'error': "No valid questions found in the response."})

    return render(request, 'quiz_nologin/basic-quiz.html')

def quiz_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    # Check if this question belongs to user's active session
    if 'active_quiz_session_id' not in request.session:
        messages.error(request, "No active quiz session found.")
        return redirect('basic-quiz')
    
    if question.session.id != request.session['active_quiz_session_id']:
        messages.error(request, "This question doesn't belong to your current quiz session.")
        return redirect('basic-quiz')
    
    # Get all questions in this session for navigation
    session_questions = question.session.questions.order_by('id')
    question_list = list(session_questions)
    
    try:
        current_index = question_list.index(question)
        next_question = question_list[current_index + 1] if current_index + 1 < len(question_list) else None
        previous_question = question_list[current_index - 1] if current_index - 1 >= 0 else None
    except ValueError:
        next_question = None
        previous_question = None
    
    # Check if user has already answered this question
    user_answer = None
    try:
        user_answer = UserAnswer.objects.get(
            session=question.session,
            question=question,
        )
    except UserAnswer.DoesNotExist:
        pass
    
    if request.method == 'POST':
        selected_option = request.POST.get('selected_option')
        if selected_option in ['A', 'B', 'C', 'D']:
            # Save or update user's answer
            user_answer, created = UserAnswer.objects.get_or_create(
                session=question.session,
                question=question,
                defaults={
                    'selected_option': selected_option,
                    'is_correct': selected_option == get_correct_letter(question)
                }
            )
            
            if not created:
                user_answer.selected_option = selected_option
                user_answer.is_correct = selected_option == get_correct_letter(question)
                user_answer.save()
            
            if next_question:
                return redirect('new-quiz', question_id=next_question.id)
            else:
                # This is the last question, redirect to results
                return redirect('quiz_results')
    
    context = {
        'question': question,
        'options': question.options.order_by('letter'),
        'next_question': next_question,
        'previous_question': previous_question,
        'current_question_number': current_index + 1 if 'current_index' in locals() else 1,
        'total_questions': len(question_list),
        'user_answer': user_answer,
    }
    
    return render(request, 'quiz_nologin/new-quiz.html', context)

def get_correct_letter(question):

    """Return the correct option letter for the given question.

    Preference order:
    1) If question.correct_answer starts with a letter like "A) ...", use that letter.
    2) Otherwise, try to match by text containment against options (case-insensitive).
    3) Fallback to 'A' if undeterminable.
    """

    if question.correct_answer:
        stripped = question.correct_answer.strip()
        if len(stripped) >= 2 and stripped[1] == ')' and stripped[0] in ['A', 'B', 'C', 'D']:
            return stripped[0]

    options = question.options.all()
    correct_answer_text = (question.correct_answer or '').lower()
    for option in options:
        if option.text.lower() in correct_answer_text or correct_answer_text in option.text.lower():
            return option.letter
    return 'A'

def quiz_results(request):
    if 'active_quiz_session_id' not in request.session:
        messages.error(request, "No active quiz session found.")
        return redirect('basic-quiz')
    
    session_id = request.session['active_quiz_session_id']
    quiz_session = get_object_or_404(QuizSession, id=session_id)
    
    # Get all user answers for this session (ensure we include every question answered)
    user_answers = UserAnswer.objects.filter(session=quiz_session).select_related('question')
    
    # Calculate score
    total_questions = quiz_session.questions.count()
    correct_answers = user_answers.filter(is_correct=True).count()
    score_percentage = ( correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Mark session as completed
    quiz_session.is_active = False
    quiz_session.save()
    
    # Clear active quiz from session
    if 'active_quiz_session_id' in request.session:
        del request.session['active_quiz_session_id']
    
    context = {
        'quiz_session': quiz_session,
        'user_answers': user_answers,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': round(score_percentage, 2),
    }
    
    return render(request, 'quiz_nologin/quiz_results.html', context)

def clear_quiz_session(request):
    """View to clear current quiz session"""
    if 'active_quiz_session_id' in request.session:
        session_id = request.session['active_quiz_session_id']
        try:
            quiz_session = QuizSession.objects.get(id=session_id)
            quiz_session.is_active = False
            quiz_session.save()
        except QuizSession.DoesNotExist:
            pass
        
        del request.session['active_quiz_session_id']
        messages.success(request, "Quiz session cleared. You can start a new quiz.")
    
    return redirect('basic-quiz')