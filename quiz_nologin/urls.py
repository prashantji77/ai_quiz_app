from urllib.parse import urlparse
from django.urls import path
from quiz_nologin import views
urlpatterns=[
    path(' ',views.save_new_quiz, name='basic-quiz'),
    path('quiz/new/<int:question_id>/', views.quiz_question, name='new-quiz'),
    path('quiz/results/', views.quiz_results, name='quiz_results'),
    path('quiz/clear/', views.clear_quiz_session, name='clear_quiz'),
]