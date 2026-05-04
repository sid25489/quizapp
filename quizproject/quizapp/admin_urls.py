"""
URL routing for Admin Quiz Management System.
Add these patterns to your main urls.py under admin namespace.
"""
from django.urls import path
from . import admin_views

# Admin URLs - included under 'admin/quiz/' in main urls.py
# DO NOT add 'quiz/' prefix here as it creates double paths like /admin/quiz/quiz/
admin_patterns = [
    # Dashboard
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Quiz Management - removed 'quiz/' prefix to avoid /admin/quiz/quiz/create/
    path('create/', admin_views.create_quiz, name='admin_create_quiz'),
    path('<int:quiz_id>/', admin_views.quiz_detail, name='admin_quiz_detail'),
    
    # Bulk Upload Flow
    path('upload/', admin_views.bulk_upload, name='admin_bulk_upload'),
    path('upload/<uuid:session_id>/preview/', admin_views.preview_upload, name='admin_preview_upload'),
    path('upload/<uuid:session_id>/success/', admin_views.upload_success, name='admin_upload_success'),
    path('upload/<uuid:session_id>/detail/', admin_views.upload_detail, name='admin_upload_detail'),
    
    # Upload History and Audit
    path('uploads/', admin_views.upload_history, name='admin_upload_history'),
    path('audit/', admin_views.audit_log, name='admin_audit_log'),
    
    # File Download
    path('upload/<uuid:session_id>/errors/download/', admin_views.download_error_report, name='admin_download_errors'),
    
    # API Endpoints
    path('api/upload/<uuid:session_id>/status/', admin_views.api_upload_status, name='api_upload_status'),
    path('api/upload/<uuid:session_id>/rollback/', admin_views.api_rollback_upload, name='api_rollback_upload'),
]

urlpatterns = admin_patterns
