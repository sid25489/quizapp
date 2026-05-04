"""
Admin views for Quiz Management System.
Handles dashboard, bulk uploads, manual entry, and audit logging.
"""
import json
import csv
from io import StringIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q
from django.core.paginator import Paginator

from .models import Quiz, Question, Choice, UploadSession, AdminAuditLog, QuestionBatch
from .admin_forms import (
    QuizCreateForm, BulkUploadForm, UploadPreviewConfirmForm,
    ManualQuestionEntryForm
)
from .services import BulkUploadService, QuizManagementService
from .file_parsers import ParserFactory


def admin_required(view_func):
    """Decorator to require admin/staff access."""
    return user_passes_test(lambda user: user.is_staff or user.is_superuser)(view_func)


@admin_required
def admin_dashboard(request):
    """
    Main admin dashboard showing:
    - Quiz management overview
    - Recent uploads
    - Pending actions
    - Audit log
    """
    
    quizzes = Quiz.objects.annotate(
        question_count=Count('questions'),
        attempt_count=Count('attempts')
    ).order_by('-updated_at')
    
    recent_uploads = UploadSession.objects.select_related('quiz', 'uploaded_by').order_by('-uploaded_at')[:10]
    recent_audit = AdminAuditLog.objects.select_related('admin_user', 'quiz').order_by('-timestamp')[:15]
    
    # Summary stats
    stats = {
        'total_quizzes': Quiz.objects.count(),
        'total_questions': Question.objects.count(),
        'total_uploads': UploadSession.objects.count(),
        'pending_uploads': UploadSession.objects.filter(status='preview_review').count(),
        'failed_uploads': UploadSession.objects.filter(status='failed').count(),
    }
    
    context = {
        'quizzes': quizzes,
        'recent_uploads': recent_uploads,
        'recent_audit': recent_audit,
        'stats': stats,
    }
    
    return render(request, 'quizapp/admin/dashboard.html', context)


@admin_required
@require_http_methods(['GET', 'POST'])
def create_quiz(request):
    """Create a new quiz."""
    
    if request.method == 'POST':
        form = QuizCreateForm(request.POST)
        if form.is_valid():
            quiz = QuizManagementService.create_quiz(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                admin_user=request.user,
                time_limit=form.cleaned_data.get('time_limit')
            )
            messages.success(request, f"Quiz '{quiz.title}' created successfully.")
            return redirect('admin_quiz_detail', quiz_id=quiz.id)
    else:
        form = QuizCreateForm()
    
    return render(request, 'quizapp/admin/create_quiz.html', {'form': form})


@admin_required
def quiz_detail(request, quiz_id):
    """View quiz details and manage questions."""
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.prefetch_related('choice_set').order_by('order')
    
    # Pagination
    paginator = Paginator(questions, 10)
    page = request.GET.get('page', 1)
    questions_page = paginator.get_page(page)
    
    context = {
        'quiz': quiz,
        'questions': questions_page,
        'total_questions': questions.count(),
    }
    
    return render(request, 'quizapp/admin/quiz_detail.html', context)


@admin_required
@require_http_methods(['GET', 'POST'])
def bulk_upload(request):
    """
    Step 1: Upload and parse file.
    """
    
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_content = file.read()
            
            try:
                # Initialize upload service
                service = BulkUploadService(request.user)
                
                # Create upload session and parse file
                session = service.start_upload(
                    file_content,
                    file.name,
                    form.cleaned_data['quiz']
                )
                
                # Parse and validate
                result = service.parse_and_validate(session)
                
                if not result['success']:
                    messages.error(request, f"Parse Error: {', '.join(result['errors'])}")
                    return render(request, 'quizapp/admin/bulk_upload.html', {'form': form})
                
                # Move to preview
                service.move_to_preview(session)
                
                messages.success(
                    request,
                    f"File parsed successfully: {result['valid_rows']} valid rows, {result['invalid_rows']} errors"
                )
                
                return redirect('admin_preview_upload', session_id=session.session_id)
            
            except Exception as e:
                messages.error(request, f"Upload failed: {str(e)}")
    else:
        form = BulkUploadForm()
    
    return render(request, 'quizapp/admin/bulk_upload.html', {'form': form})


@admin_required
def preview_upload(request, session_id):
    """
    Step 2: Preview parsed data before commit.
    """
    
    session = get_object_or_404(UploadSession, session_id=session_id)
    
    if session.status not in ['validated', 'preview_review']:
        messages.error(request, "Upload session is not in preview state.")
        return redirect('admin_dashboard')
    
    # Verify admin is the uploader
    if session.uploaded_by != request.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to view this upload.")
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = UploadPreviewConfirmForm(request.POST)
        if form.is_valid():
            # Commit upload
            service = BulkUploadService(request.user)
            success, message = service.commit_upload(session)
            
            if success:
                messages.success(request, message)
                return redirect('admin_upload_success', session_id=session.session_id)
            else:
                messages.error(request, message)
    else:
        form = UploadPreviewConfirmForm()
    
    # Get validation result from session processing
    # (This would be stored during parse_and_validate)
    validation_data = {
        'total_rows': session.total_rows,
        'valid_rows': session.valid_rows,
        'invalid_rows': session.invalid_rows,
        'duplicate_rows': session.duplicate_rows,
    }
    
    context = {
        'session': session,
        'form': form,
        'validation_data': validation_data,
    }
    
    return render(request, 'quizapp/admin/preview_upload.html', context)


@admin_required
def upload_success(request, session_id):
    """
    Step 3: Success confirmation page.
    """
    
    session = get_object_or_404(UploadSession, session_id=session_id)
    
    if session.status != 'committed':
        messages.error(request, "Upload is not in committed state.")
        return redirect('admin_dashboard')
    
    context = {
        'session': session,
        'quiz': session.quiz,
    }
    
    return render(request, 'quizapp/admin/upload_success.html', context)


@admin_required
def upload_history(request):
    """View history of all uploads for auditing."""
    
    uploads = UploadSession.objects.select_related('quiz', 'uploaded_by').order_by('-uploaded_at')
    
    # Filters
    status = request.GET.get('status')
    if status:
        uploads = uploads.filter(status=status)
    
    quiz_id = request.GET.get('quiz')
    if quiz_id:
        uploads = uploads.filter(quiz_id=quiz_id)
    
    # Pagination
    paginator = Paginator(uploads, 20)
    page = request.GET.get('page', 1)
    uploads_page = paginator.get_page(page)
    
    context = {
        'uploads': uploads_page,
        'status_choices': UploadSession.STATUS_CHOICES,
        'quizzes': Quiz.objects.all(),
    }
    
    return render(request, 'quizapp/admin/upload_history.html', context)


@admin_required
def upload_detail(request, session_id):
    """View detailed information about a specific upload."""
    
    session = get_object_or_404(UploadSession, session_id=session_id)
    
    context = {
        'session': session,
        'error_report': json.loads(session.error_report) if session.error_report else None,
    }
    
    return render(request, 'quizapp/admin/upload_detail.html', context)


@admin_required
def audit_log(request):
    """View audit trail for compliance."""
    
    logs = AdminAuditLog.objects.select_related('admin_user', 'quiz').order_by('-timestamp')
    
    # Filters
    action = request.GET.get('action')
    if action:
        logs = logs.filter(action=action)
    
    user_id = request.GET.get('user')
    if user_id:
        logs = logs.filter(admin_user_id=user_id)
    
    # Pagination
    paginator = Paginator(logs, 50)
    page = request.GET.get('page', 1)
    logs_page = paginator.get_page(page)
    
    context = {
        'logs': logs_page,
        'action_choices': AdminAuditLog.ACTION_CHOICES,
    }
    
    return render(request, 'quizapp/admin/audit_log.html', context)


@admin_required
@require_http_methods(['GET'])
def download_error_report(request, session_id):
    """Download error report as CSV."""
    
    session = get_object_or_404(UploadSession, session_id=session_id)
    
    if not session.error_report:
        messages.error(request, "No error report for this upload.")
        return redirect('admin_upload_detail', session_id=session.session_id)
    
    errors = json.loads(session.error_report).get('errors', [])
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="error_report_{session.session_id.hex[:8]}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Row Number', 'Error Message'])
    
    for error in errors:
        writer.writerow([error.get('row_number', 'N/A'), error.get('message', '')])
    
    return response


# API Endpoints for AJAX

@admin_required
@require_http_methods(['GET'])
def api_upload_status(request, session_id):
    """Get real-time upload status for AJAX polling."""
    
    session = get_object_or_404(UploadSession, session_id=session_id)
    
    return JsonResponse({
        'status': session.status,
        'total_rows': session.total_rows,
        'valid_rows': session.valid_rows,
        'invalid_rows': session.invalid_rows,
        'processed_at': session.processed_at.isoformat() if session.processed_at else None,
    })


@admin_required
@require_http_methods(['POST'])
def api_rollback_upload(request, session_id):
    """API endpoint to rollback a committed upload."""
    
    session = get_object_or_404(UploadSession, session_id=session_id)
    
    if session.status != 'committed':
        return JsonResponse({
            'success': False,
            'message': 'Only committed uploads can be rolled back.'
        })
    
    service = BulkUploadService(request.user)
    success, message = service.rollback_upload(session)
    
    return JsonResponse({
        'success': success,
        'message': message,
        'new_status': session.status
    })
