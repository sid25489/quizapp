from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, UserAnswer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    min_num = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'time_limit', 'get_questions_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'points', 'order']
    list_filter = ['quiz']
    search_fields = ['text']
    inlines = [ChoiceInline]
    ordering = ['quiz', 'order']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['text']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_score', 'is_completed', 'started_at', 'completed_at']
    list_filter = ['is_completed', 'quiz', 'started_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['started_at', 'completed_at', 'score', 'total_score']


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_choice', 'is_correct']
    list_filter = ['attempt__quiz']
    search_fields = ['attempt__user__username']
