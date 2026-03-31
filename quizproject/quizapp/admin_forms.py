"""
Forms for admin quiz management system.
Handles manual question entry and bulk upload.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Quiz, Question, Choice
import json


class QuizCreateForm(forms.ModelForm):
    """Form for creating a new quiz."""
    
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time_limit']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quiz Title',
                'required': True,
                'minlength': 3,
                'maxlength': 200,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Quiz Description',
                'rows': 4,
            }),
            'time_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Time limit in minutes (optional)',
                'min': 1,
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise ValidationError("Title must be at least 3 characters.")
        if len(title) > 200:
            raise ValidationError("Title must be under 200 characters.")
        return title
    
    def clean_time_limit(self):
        time_limit = self.cleaned_data.get('time_limit')
        if time_limit and time_limit < 1:
            raise ValidationError("Time limit must be at least 1 minute.")
        return time_limit


class QuestionForm(forms.ModelForm):
    """Form for creating/editing a single question."""
    
    # Dynamic fields for options
    options = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter options separated by | (pipe character)\nExample: Option A | Option B | Option C',
            'rows': 4,
        }),
        help_text='Separate each option with a pipe character (|)'
    )
    
    correct_answer = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Must exactly match one of the options above',
        }),
        help_text='Must match exactly one of the options'
    )
    
    class Meta:
        model = Question
        fields = ['text', 'points']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the question text',
                'rows': 3,
                'required': True,
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': 1,
                'min': 1,
                'max': 100,
            }),
        }
    
    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if len(text) < 5:
            raise ValidationError("Question must be at least 5 characters.")
        if len(text) > 1000:
            raise ValidationError("Question must be under 1000 characters.")
        return text
    
    def clean_options(self):
        """Parse and validate options."""
        options_str = self.cleaned_data['options'].strip()
        options = [opt.strip() for opt in options_str.split('|') if opt.strip()]
        
        if len(options) < 2:
            raise ValidationError("You must provide at least 2 options.")
        if len(options) > 10:
            raise ValidationError("You cannot have more than 10 options.")
        if len(set(options)) != len(options):
            raise ValidationError("Options must be unique.")
        
        return options
    
    def clean_correct_answer(self):
        """Validate correct answer matches an option."""
        correct = self.cleaned_data['correct_answer'].strip()
        options = self.clean_options()
        
        if correct not in options:
            raise ValidationError(f"Correct answer must exactly match one of the options: {', '.join(options)}")
        
        return correct
    
    def clean_points(self):
        points = self.cleaned_data['points']
        if not (1 <= points <= 100):
            raise ValidationError("Points must be between 1 and 100.")
        return points


class BulkUploadForm(forms.Form):
    """Form for bulk uploading questions from file."""
    
    quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True,
        }),
        help_text='Select the quiz to add questions to'
    )
    
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.json,.xlsx,.xls',
            'required': True,
        }),
        help_text='Supported formats: CSV, JSON, Excel (.xlsx)'
    )
    
    file_format = forms.ChoiceField(
        choices=[
            ('auto', 'Auto-detect'),
            ('csv', 'CSV'),
            ('json', 'JSON'),
            ('xlsx', 'Excel'),
        ],
        initial='auto',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        help_text='Format of the uploaded file'
    )
    
    def clean_file(self):
        """Validate file size and extension."""
        file = self.cleaned_data['file']
        
        # Max 10MB
        if file.size > 10 * 1024 * 1024:
            raise ValidationError("File size must be under 10MB.")
        
        # Check extension
        valid_extensions = ['.csv', '.json', '.xlsx', '.xls']
        import os
        file_ext = os.path.splitext(file.name)[1].lower()
        
        if file_ext not in valid_extensions:
            raise ValidationError(f"Invalid file type. Supported: {', '.join(valid_extensions)}")
        
        return file


class UploadPreviewConfirmForm(forms.Form):
    """Form for confirming upload preview before committing."""
    
    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='I have reviewed the preview and confirm to add these questions'
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Optional notes about this upload (for audit trail)',
            'rows': 3,
        })
    )


class ManualQuestionEntryForm(forms.Form):
    """Form for manually entering multiple questions at once."""
    
    questions_json = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '''[
  {
    "question": "What is 2+2?",
    "options": ["3", "4", "5"],
    "correct_answer": "4",
    "points": 1,
    "difficulty": "easy"
  }
]''',
            'rows': 15,
        }),
        help_text='Enter questions as JSON array'
    )
    
    def clean_questions_json(self):
        """Validate JSON format."""
        json_str = self.cleaned_data['questions_json'].strip()
        
        try:
            questions = json.loads(json_str)
            if not isinstance(questions, list):
                raise ValidationError("JSON must be an array of question objects.")
            return questions
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON: {str(e)}")


class QuestionSearchForm(forms.Form):
    """Form for searching and filtering questions."""
    
    quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search questions...',
        })
    )
    
    difficulty = forms.ChoiceField(
        choices=[('', 'All Difficulties'), ('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    min_points = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min points',
            'min': 0,
        })
    )
    
    max_points = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max points',
            'max': 100,
        })
    )
