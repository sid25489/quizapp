"""
Validators for bulk question/quiz uploads.
Ensures data integrity, prevents duplicates, and provides detailed error reporting.
"""
import json
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Encapsulates validation results with error details."""
    is_valid: bool
    errors: List[str]
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class QuestionValidator:
    """
    Validates individual question records.
    Checks for required fields, data types, constraints, and consistency.
    """
    
    REQUIRED_FIELDS = {'question', 'options', 'correct_answer', 'points'}
    OPTIONAL_FIELDS = {'difficulty', 'explanation', 'tags', 'time_limit'}
    
    # Constraints
    MIN_POINTS = 1
    MAX_POINTS = 100
    MIN_OPTIONS = 2
    MAX_OPTIONS = 10
    VALID_DIFFICULTIES = {'easy', 'medium', 'hard'}
    
    def validate_question(self, row: Dict[str, Any], row_number: int) -> ValidationResult:
        """Validate a single question record."""
        errors = []
        warnings = []
        
        # Check required fields
        missing_fields = self.REQUIRED_FIELDS - set(row.keys())
        if missing_fields:
            errors.append(f"Row {row_number}: Missing required fields: {', '.join(missing_fields)}")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
        
        # Validate question text
        question_text = str(row.get('question', '')).strip()
        if not question_text or len(question_text) < 5:
            errors.append(f"Row {row_number}: Question text must be at least 5 characters")
        if len(question_text) > 1000:
            errors.append(f"Row {row_number}: Question text must be under 1000 characters")
        
        # Validate options
        options_raw = row.get('options', [])
        options = self._parse_options(options_raw)
        if isinstance(options, str):  # Error message
            errors.append(f"Row {row_number}: {options}")
        else:
            if len(options) < self.MIN_OPTIONS:
                errors.append(f"Row {row_number}: Must have at least {self.MIN_OPTIONS} options")
            if len(options) > self.MAX_OPTIONS:
                errors.append(f"Row {row_number}: Cannot have more than {self.MAX_OPTIONS} options")
            
            # Check for duplicates
            if len(set(options)) != len(options):
                errors.append(f"Row {row_number}: Duplicate options detected")
        
        # Validate correct answer
        correct_answer = str(row.get('correct_answer', '')).strip()
        if correct_answer not in options:
            errors.append(f"Row {row_number}: Correct answer '{correct_answer}' not in options")
        
        # Validate points
        try:
            points = int(row.get('points', 1))
            if not (self.MIN_POINTS <= points <= self.MAX_POINTS):
                errors.append(f"Row {row_number}: Points must be between {self.MIN_POINTS} and {self.MAX_POINTS}")
        except (ValueError, TypeError):
            errors.append(f"Row {row_number}: Points must be a valid integer")
        
        # Optional field validations
        if 'difficulty' in row:
            difficulty = str(row['difficulty']).lower().strip()
            if difficulty and difficulty not in self.VALID_DIFFICULTIES:
                warnings.append(f"Row {row_number}: Unknown difficulty '{difficulty}', using default")
        
        if 'time_limit' in row:
            try:
                int(row['time_limit'])
            except (ValueError, TypeError):
                warnings.append(f"Row {row_number}: Invalid time_limit, will be ignored")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)
    
    @staticmethod
    def _parse_options(options_raw: Any) -> Tuple[List[str], str]:
        """
        Parse options from various formats.
        Returns (list, None) or (None, error_message).
        """
        if isinstance(options_raw, list):
            return [str(opt).strip() for opt in options_raw]
        elif isinstance(options_raw, str):
            # Try JSON parsing
            try:
                parsed = json.loads(options_raw)
                if isinstance(parsed, list):
                    return [str(opt).strip() for opt in parsed]
            except json.JSONDecodeError:
                pass
            
            # Try semicolon/pipe separation
            for separator in [';', '|', ',']:
                if separator in options_raw:
                    return [opt.strip() for opt in options_raw.split(separator)]
        
        return "Options format not recognized"


class QuizValidator:
    """Validates quiz metadata."""
    
    def validate_quiz(self, quiz_data: Dict[str, Any]) -> ValidationResult:
        """Validate quiz-level data."""
        errors = []
        warnings = []
        
        # Validate title
        title = str(quiz_data.get('title', '')).strip()
        if not title or len(title) < 3:
            errors.append("Quiz title must be at least 3 characters")
        if len(title) > 200:
            errors.append("Quiz title must be under 200 characters")
        
        # Validate time_limit if present
        if 'time_limit' in quiz_data:
            try:
                time_limit = int(quiz_data['time_limit'])
                if time_limit < 1:
                    errors.append("Time limit must be at least 1 minute")
            except (ValueError, TypeError):
                errors.append("Time limit must be a valid integer")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)


class DuplicateDetector:
    """Detects duplicate questions and quizzes."""
    
    @staticmethod
    def find_duplicate_questions(questions: List[Dict], existing_text: List[str]) -> List[int]:
        """
        Find rows that duplicate existing questions by text.
        Returns list of row numbers (0-indexed) that are duplicates.
        """
        duplicates = []
        seen_text = set(existing_text)
        
        for idx, question in enumerate(questions):
            question_text = str(question.get('question', '')).strip().lower()
            if question_text in seen_text:
                duplicates.append(idx)
            else:
                seen_text.add(question_text)
        
        return duplicates
    
    @staticmethod
    def find_duplicate_within_upload(questions: List[Dict]) -> List[Tuple[int, int]]:
        """
        Find duplicate question texts within the uploaded data.
        Returns list of (row1, row2) tuples that are duplicates.
        """
        duplicates = []
        seen = {}
        
        for idx, question in enumerate(questions):
            question_text = str(question.get('question', '')).strip().lower()
            if question_text in seen:
                duplicates.append((seen[question_text], idx))
            else:
                seen[question_text] = idx
        
        return duplicates


class BulkUploadValidator:
    """
    Orchestrates validation of entire bulk upload.
    Coordinates question, quiz, and duplicate validation.
    """
    
    def __init__(self):
        self.question_validator = QuestionValidator()
        self.quiz_validator = QuizValidator()
        self.duplicate_detector = DuplicateDetector()
    
    def validate_upload(
        self,
        questions: List[Dict[str, Any]],
        quiz_data: Dict[str, Any],
        existing_questions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive validation of bulk upload.
        
        Returns:
            {
                'is_valid': bool,
                'valid_rows': [],
                'invalid_rows': [{'row_number': int, 'errors': [...]}],
                'duplicate_rows': [int],
                'quiz_errors': [],
                'summary': str
            }
        """
        
        if existing_questions is None:
            existing_questions = []
        
        valid_rows = []
        invalid_rows = []
        internal_duplicates = self.duplicate_detector.find_duplicate_within_upload(questions)
        external_duplicates = self.duplicate_detector.find_duplicate_questions(
            questions,
            existing_questions
        )
        
        # Validate each question
        for row_number, question in enumerate(questions, start=1):
            # Check if external duplicate
            if row_number - 1 in external_duplicates:
                invalid_rows.append({
                    'row_number': row_number,
                    'errors': [f'Question already exists in {quiz_data.get("title", "Quiz")}']
                })
                continue
            
            # Check if internal duplicate
            if row_number - 1 in [dup[0] or dup[1] for dup in internal_duplicates]:
                invalid_rows.append({
                    'row_number': row_number,
                    'errors': ['Duplicate question within this upload']
                })
                continue
            
            # Validate question fields
            result = self.question_validator.validate_question(question, row_number)
            if result.is_valid:
                valid_rows.append(row_number)
            else:
                invalid_rows.append({
                    'row_number': row_number,
                    'errors': result.errors
                })
        
        # Validate quiz metadata
        quiz_result = self.quiz_validator.validate_quiz(quiz_data)
        quiz_errors = quiz_result.errors
        
        # Generate summary
        summary = f"Processed {len(questions)} rows: {len(valid_rows)} valid, {len(invalid_rows)} invalid"
        
        is_valid = len(valid_rows) > 0 and len(quiz_errors) == 0
        
        return {
            'is_valid': is_valid,
            'valid_rows': valid_rows,
            'invalid_rows': invalid_rows,
            'duplicate_rows': external_duplicates,
            'quiz_errors': quiz_errors,
            'summary': summary,
            'valid_count': len(valid_rows),
            'invalid_count': len(invalid_rows),
            'duplicate_count': len(external_duplicates)
        }
