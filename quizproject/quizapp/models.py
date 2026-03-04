from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_limit = models.IntegerField(help_text="Time limit in minutes", default=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_questions_count(self):
        return self.questions.count()

    def get_total_score(self):
        return sum(q.points for q in self.questions.all())


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"

    def get_correct_choice(self):
        return self.choices.filter(is_correct=True).first()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.quiz.title} - {self.score}/{self.total_score}"

    def calculate_score(self):
        correct_points = 0
        for answer in self.answers.all():
            if answer.selected_choice and answer.selected_choice.is_correct:
                correct_points += answer.question.points
        self.score = correct_points
        # total_score stays as quiz total (set at creation); don't overwrite
        if self.total_score == 0:
            self.total_score = sum(q.points for q in self.quiz.questions.all())
        self.save()
        return self.score

    def get_percentage(self):
        if self.total_score == 0:
            return 0
        return round((self.score / self.total_score) * 100, 1)


class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"{self.attempt} - {self.question.text[:30]}"

    def is_correct(self):
        if self.selected_choice:
            return self.selected_choice.is_correct
        return False
