from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count, Q, Sum
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator

from .models import Quiz, Question, Choice, QuizAttempt, UserAnswer
from .utils import can_access_attempt
from django.db import models
from .generator import generate_questions_for_topic

def generate_more(request, quiz_id):
    """Generate more questions dynamically for a specific quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # Generate 5 new questions related to the quiz title
    generated_data = generate_questions_for_topic(quiz.title, count=5)
    
    if not generated_data:
        messages.error(request, "Failed to generate new questions. Please try again later.")
        return redirect('quiz_detail', quiz_id=quiz.id)
        
    created_count = 0
    # Add new questions to the database
    current_max_order = quiz.questions.aggregate(max_order=models.Max('order'))['max_order'] or 0
    
    for i, q_data in enumerate(generated_data, start=1):
        question = Question.objects.create(
            quiz=quiz,
            text=q_data.get("text", "Unknown"),
            points=q_data.get("points", 1),
            order=current_max_order + i
        )
        for j, choice_text in enumerate(q_data.get("choices", [])):
            Choice.objects.create(
                question=question,
                text=choice_text,
                is_correct=(j == q_data.get("correct_choice_index", 0))
            )
        created_count += 1
        
    messages.success(request, f"Successfully created {created_count} more practice questions for {quiz.title}!")
    return redirect('quiz_detail', quiz_id=quiz.id)

def signup(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'quizapp/signup.html', {'form': form})


def home(request):
    """Home page displaying featured quizzes and statistics."""
    active_quizzes = Quiz.objects.filter(is_active=True)[:6]
    total_quizzes = Quiz.objects.filter(is_active=True).count()
    total_attempts = QuizAttempt.objects.filter(is_completed=True).count()
    
    context = {
        'quizzes': active_quizzes,
        'total_quizzes': total_quizzes,
        'total_attempts': total_attempts,
    }
    return render(request, 'quizapp/home.html', context)


def quiz_list(request):
    """List all available quizzes with pagination."""
    quizzes = Quiz.objects.filter(is_active=True).annotate(
        question_count=Count('questions'),
        attempt_count=Count('attempts', filter=Q(attempts__is_completed=True))
    ).order_by('-created_at')
    
    paginator = Paginator(quizzes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'quizzes': page_obj,
    }
    return render(request, 'quizapp/quiz_list.html', context)


def quiz_detail(request, quiz_id):
    """Display quiz details before starting."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    questions_count = quiz.get_questions_count()
    total_score = quiz.get_total_score()
    
    user_attempts = []
    if request.user.is_authenticated:
        user_attempts = QuizAttempt.objects.filter(
            user=request.user, 
            quiz=quiz, 
            is_completed=True
        ).order_by('-completed_at')[:5]
    
    context = {
        'quiz': quiz,
        'questions_count': questions_count,
        'total_score': total_score,
        'user_attempts': user_attempts,
    }
    return render(request, 'quizapp/quiz_detail.html', context)


def start_quiz(request, quiz_id):
    """Start a new quiz attempt."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    if quiz.get_questions_count() == 0:
        messages.error(request, "This quiz has no questions yet.")
        return redirect('quiz_detail', quiz_id=quiz_id)
    
    if not request.session.session_key:
        request.session.create()
    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key,
        total_score=quiz.get_total_score()
    )
    
    return redirect('take_quiz', attempt_id=attempt.id)


def take_quiz(request, attempt_id):
    """Display quiz questions for the user to answer."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    if attempt.is_completed:
        return redirect('quiz_result', attempt_id=attempt_id)
    
    if not can_access_attempt(attempt, request):
        messages.error(request, "You don't have permission to access this quiz attempt.")
        return redirect('home')
    
    questions = attempt.quiz.questions.prefetch_related('choices').all()
    
    existing_answers = {
        answer.question_id: answer.selected_choice_id 
        for answer in attempt.answers.all()
    }
    
    time_elapsed = (timezone.now() - attempt.started_at).total_seconds()
    time_remaining = max(0, (attempt.quiz.time_limit * 60) - time_elapsed)
    
    context = {
        'attempt': attempt,
        'quiz': attempt.quiz,
        'questions': questions,
        'existing_answers': existing_answers,
        'time_remaining': int(time_remaining),
    }
    return render(request, 'quizapp/take_quiz.html', context)


@require_POST
def save_answer(request, attempt_id):
    """Save a single answer via AJAX."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    if not can_access_attempt(attempt, request):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    if attempt.is_completed:
        return JsonResponse({'error': 'Quiz already completed'}, status=400)
    
    question_id = request.POST.get('question_id')
    choice_id = request.POST.get('choice_id')
    
    if not question_id or not choice_id:
        return JsonResponse({'error': 'Missing question or choice'}, status=400)
    
    question = get_object_or_404(Question, id=question_id, quiz=attempt.quiz)
    choice = get_object_or_404(Choice, id=choice_id, question=question)
    
    answer, created = UserAnswer.objects.update_or_create(
        attempt=attempt,
        question=question,
        defaults={'selected_choice': choice}
    )
    
    return JsonResponse({
        'success': True,
        'question_id': question_id,
        'choice_id': choice_id,
        'is_new': created
    })


@require_POST
def submit_quiz(request, attempt_id):
    """Submit the quiz and calculate the score."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    if not can_access_attempt(attempt, request):
        messages.error(request, "You don't have permission to submit this quiz.")
        return redirect('home')
    
    if attempt.is_completed:
        messages.info(request, "This quiz has already been submitted.")
        return redirect('quiz_result', attempt_id=attempt_id)
    
    questions = attempt.quiz.questions.all()
    for question in questions:
        choice_id = request.POST.get(f'question_{question.id}')
        if choice_id:
            choice = get_object_or_404(Choice, id=choice_id, question=question)
            UserAnswer.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={'selected_choice': choice}
            )
    
    attempt.calculate_score()
    attempt.is_completed = True
    attempt.completed_at = timezone.now()
    attempt.save()
    
    messages.success(request, f"Quiz submitted! You scored {attempt.score}/{attempt.total_score}")
    return redirect('quiz_result', attempt_id=attempt_id)


def quiz_result(request, attempt_id):
    """Display quiz results with detailed breakdown."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    if not can_access_attempt(attempt, request):
        messages.error(request, "You don't have permission to view this result.")
        return redirect('home')
    
    if not attempt.is_completed:
        return redirect('take_quiz', attempt_id=attempt_id)
    
    answers_by_question = {a.question_id: a for a in attempt.answers.select_related('selected_choice').all()}
    questions_with_answers = []
    for question in attempt.quiz.questions.prefetch_related('choices').all():
        user_answer = answers_by_question.get(question.id)
        questions_with_answers.append({
            'question': question,
            'choices': question.choices.all(),
            'user_answer': user_answer,
            'selected_choice': user_answer.selected_choice if user_answer else None,
            'correct_choice': question.get_correct_choice(),
            'is_correct': user_answer.is_correct() if user_answer else False,
        })
    
    quiz_stats = QuizAttempt.objects.filter(
        quiz=attempt.quiz,
        is_completed=True
    ).aggregate(
        avg_score=Avg('score'),
        total_attempts=Count('id')
    )
    
    context = {
        'attempt': attempt,
        'quiz': attempt.quiz,
        'questions_with_answers': questions_with_answers,
        'percentage': attempt.get_percentage(),
        'quiz_stats': quiz_stats,
    }
    return render(request, 'quizapp/quiz_result.html', context)


def leaderboard(request, quiz_id):
    """Display leaderboard for a specific quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    top_attempts = QuizAttempt.objects.filter(
        quiz=quiz,
        is_completed=True
    ).select_related('user').order_by('-score', 'completed_at')[:20]
    
    context = {
        'quiz': quiz,
        'top_attempts': top_attempts,
    }
    return render(request, 'quizapp/leaderboard.html', context)


@login_required
def my_attempts(request):
    """Display user's quiz history."""
    attempts_qs = QuizAttempt.objects.filter(
        user=request.user,
        is_completed=True
    ).select_related('quiz').order_by('-completed_at')
    
    paginator = Paginator(attempts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    agg = attempts_qs.aggregate(
        total_attempts=Count('id'),
        total_score_sum=Sum('score'),
        total_possible_sum=Sum('total_score')
    )
    avg_pct = 0
    if agg['total_possible_sum'] and agg['total_possible_sum'] > 0:
        avg_pct = round(agg['total_score_sum'] * 100 / agg['total_possible_sum'], 1)
    stats = {
        'total_attempts': agg['total_attempts'],
        'avg_percentage': avg_pct
    }
    
    context = {
        'page_obj': page_obj,
        'attempts': page_obj,
        'stats': stats,
    }
    return render(request, 'quizapp/my_attempts.html', context)


def quiz_api_list(request):
    """API endpoint to get list of quizzes as JSON."""
    quizzes = Quiz.objects.filter(is_active=True).prefetch_related('questions')
    quiz_list = [
        {
            'id': q.id,
            'title': q.title,
            'description': q.description,
            'time_limit': q.time_limit,
            'created_at': q.created_at.isoformat() if q.created_at else None,
            'questions_count': q.questions.count(),
            'total_score': sum(qu.points for qu in q.questions.all()),
        }
        for q in quizzes
    ]
    return JsonResponse({'quizzes': quiz_list}, safe=False)


def quiz_api_detail(request, quiz_id):
    """API endpoint to get quiz details with questions."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    questions_data = []
    for question in quiz.questions.all():
        choices_data = [
            {'id': c.id, 'text': c.text} 
            for c in question.choices.all()
        ]
        questions_data.append({
            'id': question.id,
            'text': question.text,
            'points': question.points,
            'choices': choices_data
        })
    
    data = {
        'id': quiz.id,
        'title': quiz.title,
        'description': quiz.description,
        'time_limit': quiz.time_limit,
        'questions_count': quiz.get_questions_count(),
        'total_score': quiz.get_total_score(),
        'questions': questions_data
    }
    
    return JsonResponse(data)
