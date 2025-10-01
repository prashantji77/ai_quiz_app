from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quizapp.models import QuizSession

@login_required
def sessions_list_view(request):
    sessions = QuizSession.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "quiz/sessions.html", {"sessions": sessions})