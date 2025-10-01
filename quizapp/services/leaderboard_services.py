
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.db.models import Sum,Q,Max

def get_top_user(limit=50):
    top_user=(
    User.objects.filter(is_staff=False, is_superuser=False)
    .annotate(
        total_score=Coalesce(Sum("quiz_sessions__score", filter=Q(quiz_sessions__is_active=False)),0),
        total_questions=Coalesce(Sum("quiz_sessions__total_questions", filter=Q(quiz_sessions__is_active=False)),0),
        last_played=Max("quiz_sessions__created_at"),
        )
        .order_by("-total_score", "-total_questions","-last_played")[:limit]
    )
    return top_user