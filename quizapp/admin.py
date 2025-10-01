from django.contrib import admin
from .models import Question, Option, Profile,Result,QuizSession
# Register your models here.
@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'text', 'correct_answer']

@admin.register(Option)
class OptionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'text']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_quiz_active']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display=['id','user','question','selected_option','correct_answer_snapshot','options_snapshot','is_correct','created_at']

@admin.register(QuizSession)
class SessionAdmin(admin.ModelAdmin):
    list_display=['id','user','title','created_at','is_active']