from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_sessions')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.title or 'Session'} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Question(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.text[:50]

class Option(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_quiz_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Use a signal to automatically create/update a Profile when a User is created/saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='results', null=True, blank=True)
    question = models.ForeignKey(Question, related_name="results", on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    correct_answer_snapshot = models.CharField(max_length=255)
    options_snapshot = models.JSONField(default=list)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.id} - {'✔' if self.is_correct else '✘'}"
