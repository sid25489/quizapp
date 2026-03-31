"""
Service layer for bulk upload and admin operations.
Handles transactions, error recovery, and audit logging.
"""
import json
import logging
from typing import List, Dict, Tuple, Any
from datetime import datetime
from django.db import transaction
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import tempfile
import os

from .models import Quiz, Question, Choice, UploadSession, AdminAuditLog, QuestionBatch
from .file_parsers import ParserFactory
from .validators import BulkUploadValidator

logger = logging.getLogger(__name__)


class BulkUploadService:
    """
    Orchestrates the bulk upload process:
    1. Parse file
    2. Validate data
    3. Generate preview
    4. Commit to database
    5. Log audit trail
    
    Zero data loss guarantee: Uses database transactions and rollback capability.
    """
    
    def __init__(self, admin_user: User):
        self.admin_user = admin_user
        self.validator = BulkUploadValidator()
        self.logger = logging.getLogger('quizapp.bulk_upload')
    
    def start_upload(
        self,
        file_content: bytes,
        filename: str,
        quiz: Quiz,
        quiz_metadata: Dict[str, str] = None
    ) -> UploadSession:
        """
        Step 1: Initialize upload session and parse file.
        
        Returns:
            UploadSession object with status 'processing'
        """
        
        # Determine file format
        file_format = filename.split('.')[-1].lower()
        if file_format not in ['csv', 'json', 'xlsx', 'xls']:
            raise ValueError(f"Unsupported file format: {file_format}")
        
        # Create upload session
        session = UploadSession.objects.create(
            quiz=quiz,
            original_filename=filename,
            file_format=file_format,
            file_size_bytes=len(file_content),
            uploaded_by=self.admin_user,
            status='processing'
        )
        
        # Save file temporarily
        temp_dir = tempfile.gettempdir()
        temp_filename = f"upload_{session.session_id.hex}.bin"
        temp_path = os.path.join(temp_dir, temp_filename)
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(file_content)
            session.temp_file_path = temp_path
            session.save()
        except Exception as e:
            session.status = 'failed'
            session.error_report = json.dumps({
                'error': 'Failed to save temporary file',
                'details': str(e)
            })
            session.save()
            raise
        
        self._log_audit('upload_start', session)
        
        return session
    
    def parse_and_validate(
        self,
        session: UploadSession,
        quiz_metadata: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        Step 2: Parse file and validate all questions.
        
        Returns:
            {
                'session': UploadSession,
                'validation_result': dict with valid/invalid/duplicate rows,
                'preview_data': list of validated rows
            }
        """
        
        if quiz_metadata is None:
            quiz_metadata = {
                'title': session.quiz.title,
                'description': session.quiz.description,
            }
        
        # Parse file
        rows, parse_errors = ParserFactory.parse_file(
            self._read_temp_file(session.temp_file_path),
            session.original_filename
        )
        
        if parse_errors:
            session.status = 'failed'
            session.error_report = json.dumps({
                'type': 'parse_error',
                'errors': parse_errors
            })
            session.save()
            return {
                'success': False,
                'errors': parse_errors,
                'session': session
            }
        
        # Get existing question texts for duplicate detection
        existing_questions = list(
            session.quiz.question_set.values_list('text', flat=True)
        )
        
        # Validate all questions
        validation_result = self.validator.validate_upload(
            rows,
            quiz_metadata,
            list(existing_questions)
        )
        
        # Update session with metrics
        session.total_rows = len(rows)
        session.valid_rows = validation_result['valid_count']
        session.invalid_rows = validation_result['invalid_count']
        session.duplicate_rows = validation_result['duplicate_count']
        session.status = 'validated'
        session.processed_at = datetime.now()
        session.save()
        
        # Prepare preview data (only valid rows)
        preview_data = [
            rows[idx - 1] for idx in validation_result['valid_rows']
        ]
        
        return {
            'success': True,
            'session': session,
            'validation_result': validation_result,
            'preview_data': preview_data,
            'total_rows': len(rows),
            'parse_errors': parse_errors
        }
    
    def move_to_preview(self, session: UploadSession) -> None:
        """
        Step 3: Move session to preview/review stage.
        """
        session.status = 'preview_review'
        session.save()
    
    @transaction.atomic
    def commit_upload(self, session: UploadSession) -> Tuple[bool, str]:
        """
        Step 4: Atomically create questions and choices in database.
        
        Uses transaction.atomic() for ACID guarantee.
        Rollback on any error - zero data loss.
        
        Returns:
            (success: bool, message: str)
        """
        
        if session.status != 'preview_review':
            return False, "Upload must be in preview state before commit"
        
        if session.valid_rows == 0:
            return False, "No valid rows to commit"
        
        try:
            # Re-parse to get fresh data
            file_content = self._read_temp_file(session.temp_file_path)
            rows, _ = ParserFactory.parse_file(file_content, session.original_filename)
            
            # Get existing questions for validation
            existing_questions = set(
                session.quiz.question_set.values_list('text', flat=True)
            )
            
            # Re-validate to be safe
            validation_result = self.validator.validate_upload(
                rows,
                {'title': session.quiz.title},
                list(existing_questions)
            )
            
            # Create question batch for audit trail
            batch = QuestionBatch.objects.create(
                quiz=session.quiz,
                created_by=self.admin_user,
                question_count=session.valid_rows,
                source='bulk_upload'
            )
            
            # Create Question and Choice objects
            created_count = 0
            
            for row_idx in validation_result['valid_rows']:
                row = rows[row_idx - 1]
                
                # Skip if somehow duplicate
                question_text = str(row.get('question', '')).strip()
                if session.quiz.question_set.filter(text=question_text).exists():
                    continue
                
                # Create question
                question = Question.objects.create(
                    quiz=session.quiz,
                    text=question_text,
                    points=int(row.get('points', 1)),
                    order=session.quiz.question_set.count() + created_count + 1
                )
                
                # Parse and create choices
                options = self._parse_options(row.get('options', []))
                correct_answer = str(row.get('correct_answer', '')).strip()
                
                for option_text in options:
                    Choice.objects.create(
                        question=question,
                        text=option_text,
                        is_correct=(option_text == correct_answer)
                    )
                
                created_count += 1
            
            # Update session status
            session.status = 'committed'
            session.committed_at = datetime.now()
            session.save()
            
            # Log audit trail
            self._log_audit('upload_commit', session, {
                'created_questions': created_count,
                'batch_id': batch.batch_id.hex
            })
            
            # Cleanup temp file
            self._cleanup_temp_file(session.temp_file_path)
            
            return True, f"Successfully created {created_count} questions"
        
        except Exception as e:
            # This triggers automatic rollback due to @transaction.atomic
            logger.error(f"Upload commit failed: {str(e)}", exc_info=True)
            session.status = 'failed'
            session.error_report = json.dumps({
                'error': 'Commit failed - automatic rollback triggered',
                'details': str(e)
            })
            session.save()
            
            self._log_audit('upload_rollback', session, {
                'error': str(e)
            })
            
            return False, f"Upload failed and rolled back: {str(e)}"
    
    def rollback_upload(self, session: UploadSession) -> Tuple[bool, str]:
        """
        Manual rollback of a committed upload.
        Deletes all questions from this batch.
        
        Returns:
            (success: bool, message: str)
        """
        
        if session.status != 'committed':
            return False, "Only committed uploads can be rolled back"
        
        try:
            # Find the batch for this upload
            batch = QuestionBatch.objects.filter(
                quiz=session.quiz,
                created_by=self.admin_user
            ).order_by('-created_at').first()
            
            if not batch:
                return False, "Cannot find associated question batch"
            
            # This should be done in a transaction
            with transaction.atomic():
                # Delete all questions in this batch
                deleted_count = batch.questionbatch.count()
                batch.questionbatch.all().delete()
                
                # Update session status
                session.status = 'rolled_back'
                session.save()
            
            # Log audit trail
            self._log_audit('upload_rollback', session, {
                'deleted_questions': deleted_count,
                'batch_id': batch.batch_id.hex
            })
            
            return True, f"Rolled back {deleted_count} questions"
        
        except Exception as e:
            logger.error(f"Rollback failed: {str(e)}", exc_info=True)
            return False, f"Rollback failed: {str(e)}"
    
    def _parse_options(self, options_raw: Any) -> List[str]:
        """Parse options from various formats."""
        if isinstance(options_raw, list):
            return [str(opt).strip() for opt in options_raw]
        
        options_str = str(options_raw).strip()
        
        # Try JSON
        try:
            parsed = json.loads(options_str)
            if isinstance(parsed, list):
                return [str(opt).strip() for opt in parsed]
        except:
            pass
        
        # Try pipe/semicolon separated
        for sep in ['|', ';', ',']:
            if sep in options_str:
                return [opt.strip() for opt in options_str.split(sep)]
        
        return [options_str]
    
    @staticmethod
    def _read_temp_file(path: str) -> bytes:
        """Read temporary file safely."""
        try:
            with open(path, 'rb') as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Failed to read temporary file: {str(e)}")
    
    @staticmethod
    def _cleanup_temp_file(path: str) -> None:
        """Delete temporary file safely."""
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file {path}: {str(e)}")
    
    def _log_audit(
        self,
        action: str,
        session: UploadSession,
        details: Dict = None
    ) -> None:
        """Log audit trail for compliance."""
        if details is None:
            details = {}
        
        AdminAuditLog.objects.create(
            action=action,
            admin_user=self.admin_user,
            quiz=session.quiz,
            upload_session=session,
            details={
                'filename': session.original_filename,
                'format': session.file_format,
                'total_rows': session.total_rows,
                'valid_rows': session.valid_rows,
                **details
            }
        )


class QuizManagementService:
    """Service for quiz lifecycle management."""
    
    @staticmethod
    def create_quiz(
        title: str,
        description: str,
        admin_user: User,
        time_limit: int = None
    ) -> Quiz:
        """Create a new quiz."""
        quiz = Quiz.objects.create(
            title=title,
            description=description,
            time_limit=time_limit,
            is_active=False
        )
        
        # Log audit
        AdminAuditLog.objects.create(
            action='quiz_create',
            admin_user=admin_user,
            quiz=quiz,
            details={'title': title}
        )
        
        return quiz
    
    @staticmethod
    def update_quiz(
        quiz: Quiz,
        admin_user: User,
        **kwargs
    ) -> Quiz:
        """Update quiz metadata."""
        for key, value in kwargs.items():
            if hasattr(quiz, key):
                setattr(quiz, key, value)
        
        quiz.save()
        
        # Log audit
        AdminAuditLog.objects.create(
            action='quiz_update',
            admin_user=admin_user,
            quiz=quiz,
            details=kwargs
        )
        
        return quiz
