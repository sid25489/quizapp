import json
import csv
import io
from pathlib import Path
from django.utils import timezone
from .models import Question, Quiz, Choice
from .ai_engine.validator import AIValidator
from .ai_engine.similarity import SimilarityEngine

class SmartIngestionPipeline:
    def __init__(self, quiz):
        self.quiz = quiz
        self.validator = AIValidator()
        self.similarity = SimilarityEngine()
        
    def process_file(self, file_content, filename):
        ext = Path(filename).suffix.lstrip('.').lower()
        rows = []
        if ext == 'csv':
            text_content = file_content.decode('utf-8')
            reader = csv.DictReader(io.StringIO(text_content))
            for row in reader:
                rows.append(row)
        elif ext == 'json':
            text_content = file_content.decode('utf-8')
            data = json.loads(text_content)
            if isinstance(data, list):
                rows = data
            elif 'questions' in data:
                rows = data['questions']
            else:
                raise ValueError("Invalid JSON structure")
        else:
            raise ValueError(f"Unsupported format: {ext}")
            
        accepted_questions = []
        rejected_questions = []
        
        # We can fetch existing questions embeddings for duplicate check
        existing_questions = list(Question.objects.filter(quiz=self.quiz).values_list('text', flat=True))
        
        for row in rows:
            q_text = row.get('question', '')
            options = []
            if 'options' in row and isinstance(row['options'], list):
                options = row['options']
            else:
                for key in row.keys():
                    if key.startswith('option'):
                        options.append(row[key])
            
            correct = row.get('correct_option', row.get('correct', row.get('correct_answer', '')))
            
            # AI Validation
            validation = self.validator.validate_question(q_text, options, correct)
            
            # Smart Duplicate Check
            is_dup = validation.get('duplicate', False)
            if not is_dup:
                # DB Exact Check
                if Question.objects.filter(quiz=self.quiz, text__iexact=validation.get('corrected_question', q_text)).exists():
                    is_dup = True
                else:
                    # Semantic Similarity Check
                    for eq in existing_questions:
                        if self.similarity.is_duplicate(validation.get('corrected_question', q_text), eq):
                            is_dup = True
                            break
            
            validation['duplicate'] = is_dup
            
            # Check validation rules
            quality = validation.get('quality_score', 0)
            is_valid = validation.get('is_valid', False)
            
            if is_valid and quality >= 60 and not is_dup:
                # Store
                q = Question.objects.create(
                    quiz=self.quiz,
                    text=validation.get('corrected_question', q_text),
                    difficulty=validation.get('difficulty', 'Medium'),
                    tags=validation.get('tags', []),
                    quality_score=quality,
                    ai_validated=True,
                    original_text=q_text
                )
                
                corrected_options = validation.get('corrected_options', options)
                correct_ans = validation.get('correct_answer', correct)
                
                for opt in corrected_options:
                    Choice.objects.create(
                        question=q,
                        text=opt,
                        is_correct=(opt.strip().lower() == str(correct_ans).strip().lower())
                    )
                
                accepted_questions.append(validation)
                existing_questions.append(q.text)
            else:
                rejected_questions.append(validation)
                
        # Generate Logs
        # In a real app we might write this to S3 or local disk. For now we will return them.
        return accepted_questions, rejected_questions

