# ...existing code...
from django.contrib import admin
from .models import Question, Option, UserAnswer, QuizSession
# Register your models here.

@admin.register(Question)
class NewQuestionModelAdmin(admin.ModelAdmin):
    list_display = ['id','session','text', 'correct_answer','created_at']

@admin.register(Option)
class NewOptionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text','letter']


@admin.register(UserAnswer)
class NewUserAnswerModelAdmin(admin.ModelAdmin):
    list_display=['id','question','selected_option','correct_answer_snapshot','options_snapshot','is_correct','created_at']

    # Added methods so list_display can show snapshots even if they are not model fields
    def options_snapshot(self, obj):
        val = getattr(obj, 'options_snapshot', None)
        # If stored as list/tuple (e.g. JSONField), join for display; otherwise show raw value
        if isinstance(val, (list, tuple)):
            return ', '.join(str(x) for x in val)
        return str(val) if val is not None else '-'
    options_snapshot.short_description = 'Options'

    def correct_answer_snapshot(self, obj):
        val = getattr(obj, 'correct_answer_snapshot', None)
        return str(val) if val is not None else '-'
    correct_answer_snapshot.short_description = 'Correct Answer'

@admin.register(QuizSession)
class NewQuizSessionModelAdmin(admin.ModelAdmin):
    list_display=['id','session_key','title','created_at','is_active']
# ...existing code...