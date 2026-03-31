"""
Extended models for Admin Practice Quiz Management System.
These models support bulk uploads, versioning, and audit logging.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class QuizVersion(models.Model):
    """Tracks quiz versions for rollback capability."""
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('quiz', 'version_number')
        ordering = ['-version_number']
    
    def __str__(self):
        return f"{self.quiz.title} v{self.version_number}"


class QuestionBatch(models.Model):
    """Track batches of questions for audit and rollback."""
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='question_batches')
    batch_id = models.UUIDField(default=uuid.uuid4, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    question_count = models.IntegerField()
    source = models.CharField(
        max_length=50,
        choices=[
            ('manual', 'Manual Entry'),
            ('bulk_upload', 'Bulk Upload'),
            ('ai_generated', 'AI Generated'),
        ],
        default='manual'
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.quiz.title} - Batch {self.batch_id.hex[:8]}"


class UploadSession(models.Model):
    """
    Critical model for bulk upload tracking.
    Enables debugging, audit logging, and rollback capability.
    """
    
    STATUS_CHOICES = [
        ('upload_pending', 'Upload Pending'),
        ('processing', 'Processing'),
        ('validated', 'Validated'),
        ('preview_review', 'Preview Review'),
        ('committed', 'Committed'),
        ('failed', 'Failed'),
        ('rolled_back', 'Rolled Back'),
    ]
    
    # Core Fields
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, null=True, blank=True, related_name='upload_sessions')
    
    # File Metadata
    original_filename = models.CharField(max_length=255)
    file_format = models.CharField(
        max_length=10,
        choices=[
            ('csv', 'CSV'),
            ('json', 'JSON'),
            ('xlsx', 'Excel'),
        ],
        default='csv'
    )
    file_size_bytes = models.BigIntegerField()
    
    # Status Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upload_pending')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    committed_at = models.DateTimeField(null=True, blank=True)
    
    # Processing Metrics
    total_rows = models.IntegerField(default=0)
    valid_rows = models.IntegerField(default=0)
    invalid_rows = models.IntegerField(default=0)
    duplicate_rows = models.IntegerField(default=0)
    
    # Error Handling
    error_report = models.TextField(blank=True)  # JSON format
    error_file_path = models.CharField(max_length=500, blank=True)
    
    # Confidential
    temp_file_path = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['status', '-uploaded_at']),
            models.Index(fields=['uploaded_by', '-uploaded_at']),
        ]
    
    def __str__(self):
        return f"Upload {self.session_id.hex[:8]} - {self.original_filename}"
    
    @property
    def success_rate_percent(self):
        """Calculate validation success rate."""
        if self.total_rows == 0:
            return 0
        return round((self.valid_rows / self.total_rows) * 100, 2)
    
    @property
    def can_commit(self):
        """Check if upload can be committed."""
        return self.status == 'preview_review' and self.valid_rows > 0


class AdminAuditLog(models.Model):
    """
    Audit trail for all admin actions.
    Enables compliance, security analysis, and troubleshooting.
    """
    
    ACTION_CHOICES = [
        ('quiz_create', 'Quiz Created'),
        ('quiz_update', 'Quiz Updated'),
        ('quiz_delete', 'Quiz Deleted'),
        ('upload_start', 'Upload Started'),
        ('upload_commit', 'Upload Committed'),
        ('upload_rollback', 'Upload Rolled Back'),
        ('question_batch_delete', 'Question Batch Deleted'),
        ('quiz_version_create', 'Quiz Version Created'),
    ]
    
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    quiz = models.ForeignKey('Quiz', on_delete=models.SET_NULL, null=True, blank=True)
    upload_session = models.ForeignKey(UploadSession, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['admin_user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.get_action_display()} by {self.admin_user.username} at {self.timestamp}"
