# models.py
from django.db import models
import uuid

class QuizSession(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.session_key})"

class Question(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text[:50]  # First 50 chars

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    letter = models.CharField(max_length=1)  # A, B, C, D
    
    def __str__(self):
        return f"{self.letter}) {self.text}"

class UserAnswer(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)  # A, B, C, D
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)