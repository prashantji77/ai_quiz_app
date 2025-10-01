from django.urls import path
from django.contrib.auth import views as login_auth_views
from.forms import (
    CustomerLoginForm,)
from quizapp.views import auth_views,quiz_views,result_views,session_views,home_views

urlpatterns = [
    #Home / Index
    path('', home_views.index),
    path('quiz/', home_views.home, name='home'),

    # Registration & Authentication
    path('registration/', auth_views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/',login_auth_views.LoginView.as_view(template_name='app/login.html',
        authentication_form= CustomerLoginForm),name='login'),
    path('accounts/logout/', auth_views.logout_view, name='logout'),
    
    #Quiz Flow
    path("quiz/<int:question_id>/", quiz_views.quiz_view, name="quiz"),
    path('quiz/finish/', quiz_views.finish_quiz, name='finish_quiz'),
    path('maths-quiz/', quiz_views.save_quiz, name='maths-quiz'),

    #Result
    path('quiz/results/', result_views.results_view, name='quiz_results'),
    path('quiz/results/<int:session_id>/', result_views.results_view_session, name='quiz_results_session'),

    #Sesson
    path('sessions/', session_views.sessions_list_view, name='quiz_sessions'),

    #Leaderboard
    path('quiz/leaderboard/', result_views.leaderboard_view, name='quiz_leaderboard'),

]