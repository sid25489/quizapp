"""
File parsers for bulk upload system.
Handles CSV, JSON, and Excel formats with error recovery.
"""
import csv
import json
import io
from typing import List, Dict, Tuple, Any
from pathlib import Path


class CSVParser:
    """Parse and validate CSV files for bulk question upload."""
    
    @staticmethod
    def parse(file_content: bytes) -> Tuple[List[Dict], List[str]]:
        """
        Parse CSV file content.
        
        Expected columns: question, options, correct_answer, points, [difficulty, explanation, tags]
        
        Returns:
            (list of dicts, list of errors)
        """
        errors = []
        rows = []
        
        try:
            text_content = file_content.decode('utf-8')
        except UnicodeDecodeError:
            return [], ["File encoding error: File must be UTF-8 encoded"]
        
        try:
            reader = csv.DictReader(io.StringIO(text_content))
            
            if not reader.fieldnames:
                return [], ["CSV file is empty or has no headers"]
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                try:
                    # Clean whitespace
                    cleaned_row = {k.strip().lower(): v.strip() if v else '' for k, v in row.items()}
                    rows.append(cleaned_row)
                except Exception as e:
                    errors.append(f"Row {row_num}: Failed to parse - {str(e)}")
            
            if not rows:
                errors.append("No data rows found in CSV file")
        
        except Exception as e:
            errors.append(f"CSV parsing error: {str(e)}")
        
        return rows, errors


class JSONParser:
    """Parse and validate JSON files for bulk question upload."""
    
    @staticmethod
    def parse(file_content: bytes) -> Tuple[List[Dict], List[str]]:
        """
        Parse JSON file content.
        
        Expected format:
        {
            "quiz": {"title": "...", "description": "..."},
            "questions": [
                {"question": "...", "options": [...], "correct_answer": "...", "points": ...},
                ...
            ]
        }
        
        Returns:
            (list of question dicts, list of errors)
        """
        errors = []
        rows = []
        
        try:
            text_content = file_content.decode('utf-8')
            data = json.loads(text_content)
        except UnicodeDecodeError:
            return [], ["File encoding error: File must be UTF-8 encoded"]
        except json.JSONDecodeError as e:
            return [], [f"Invalid JSON format: {str(e)}"]
        
        try:
            # Check structure
            if not isinstance(data, dict):
                return [], ["JSON must be an object at root level"]
            
            if 'questions' not in data:
                return [], ["JSON must contain 'questions' key"]
            
            questions = data.get('questions', [])
            if not isinstance(questions, list):
                return [], ["'questions' must be an array"]
            
            if not questions:
                errors.append("No questions found in JSON")
                return [], errors
            
            # Parse each question
            for idx, question in enumerate(questions):
                if not isinstance(question, dict):
                    errors.append(f"Question {idx + 1}: Must be an object")
                    continue
                
                # Normalize keys to lowercase
                normalized = {k.lower(): v for k, v in question.items()}
                rows.append(normalized)
        
        except Exception as e:
            errors.append(f"JSON parsing error: {str(e)}")
        
        return rows, errors


class ExcelParser:
    """Parse Excel (.xlsx) files for bulk question upload."""
    
    @staticmethod
    def parse(file_content: bytes) -> Tuple[List[Dict], List[str]]:
        """
        Parse Excel file content.
        
        Expected: First worksheet with headers in row 1.
        Columns: question, options, correct_answer, points, [difficulty, explanation, tags]
        
        Returns:
            (list of dicts, list of errors)
        """
        errors = []
        rows = []
        
        try:
            import openpyxl
        except ImportError:
            return [], ["Excel support requires openpyxl: pip install openpyxl"]
        
        try:
            workbook = openpyxl.load_workbook(io.BytesIO(file_content))
            worksheet = workbook.active
            
            # Get headers
            headers = []
            for cell in worksheet[1]:
                if cell.value:
                    headers.append(str(cell.value).strip().lower())
            
            if not headers:
                return [], ["Excel file has no headers in first row"]
            
            # Get data rows
            for row_num, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
                if not any(row):  # Skip empty rows
                    continue
                
                row_dict = {}
                for col_idx, (header, value) in enumerate(zip(headers, row)):
                    if value is not None:
                        row_dict[header] = str(value).strip()
                
                if row_dict:  # Only add non-empty rows
                    rows.append(row_dict)
            
            if not rows:
                errors.append("No data rows found in Excel file")
        
        except Exception as e:
            errors.append(f"Excel parsing error: {str(e)}")
        
        return rows, errors


class ParserFactory:
    """Factory for selecting appropriate parser based on file format."""
    
    PARSERS = {
        'csv': CSVParser,
        'json': JSONParser,
        'xlsx': ExcelParser,
        'xls': ExcelParser,  # For compatibility
    }
    
    @classmethod
    def get_parser(cls, filename: str):
        """Get parser for file extension."""
        ext = Path(filename).suffix.lstrip('.').lower()
        return cls.PARSERS.get(ext)
    
    @classmethod
    def parse_file(cls, file_content: bytes, filename: str) -> Tuple[List[Dict], List[str]]:
        """
        Parse file using appropriate parser based on extension.
        
        Returns:
            (list of question dicts, list of errors)
        """
        parser_class = cls.get_parser(filename)
        
        if not parser_class:
            ext = Path(filename).suffix.lstrip('.')
            return [], [f"Unsupported file format: .{ext}. Supported formats: CSV, JSON, XLSX"]
        
        return parser_class.parse(file_content)
