
from quizapp.models import Result,Question,QuizSession
from django.contrib.auth.decorators import login_required
import requests,json
from django.shortcuts import get_object_or_404,render
from quizapp.services.result_services import calculate_score

@login_required
def results_view(request):
    user = request.user
    results = Result.objects.filter(user=user).select_related('question').order_by('created_at')
    score , total_questions, breakdown = calculate_score(results)
    return render(request, 'quiz/results.html', {
        'score': score,
        'total_questions': total_questions,
        'breakdown': breakdown,
    })

@login_required
def results_view_session(request, session_id):
    user = request.user
    session = get_object_or_404(QuizSession, id=session_id, user=user)
    results = Result.objects.filter(user=user, session=session).select_related('question').order_by('created_at')
    score, total_questions, breakdown= calculate_score(results)
    score_percentage=(score/total_questions * 100) if total_questions > 0 else 0
    return render(request, 'quiz/results.html', {
        'score': score,
        'total_questions': total_questions,
        'breakdown': breakdown,
        'session': session,
        'score_percentage':score_percentage
    })


@login_required
def leaderboard_view(request):
    from quizapp.services.leaderboard_services import get_top_user
    # Aggregate totals per user (include users with no sessions as 0)
    top_users=get_top_user()
    return render(request, 'quiz/leaderboard.html', { 'top_users': top_users, 'current_user_id': request.user.id })
