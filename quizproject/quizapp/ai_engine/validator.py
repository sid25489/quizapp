import json
import os
import google.generativeai as genai

# Initialize Gemini API
# Assuming API key is in environment variable GOOGLE_API_KEY
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))

class AIValidator:
    def __init__(self):
        # We can use gemini-1.5-flash
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def validate_question(self, question_text, options, correct_option=None):
        """
        Validates clarity, single correct answer, ambiguity, grammar, normalizes options.
        Returns a dictionary in the strict JSON response format.
        """
        prompt = f"""
        You are an expert educational content validator. Review the following multiple-choice question.
        
        Question: {question_text}
        Options: {options}
        Correct Option (if provided): {correct_option}
        
        Your tasks:
        1. Validate clarity and correctness.
        2. Ensure there is exactly one correct answer.
        3. Detect any ambiguity.
        4. Fix grammar and structure.
        5. Normalize options (e.g., consistent capitalization).
        6. Assign a QUALITY SCORE (0-100).
        7. Provide a corrected version of the question and options.
        8. Classify difficulty as 'Easy', 'Medium', or 'Hard'.
        9. Generate 3-5 relevant tags (topic, subtopic, concepts).
        
        You MUST respond ONLY with a raw JSON object (no markdown formatting, no code blocks) matching exactly this schema:
        {{
            "is_valid": true/false,
            "quality_score": number,
            "issues": ["list of issues found"],
            "corrected_question": "string",
            "corrected_options": ["string"],
            "correct_answer": "string",
            "duplicate": false,
            "difficulty": "Easy|Medium|Hard",
            "tags": ["tag1", "tag2"]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean up the response if it has markdown formatting
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            result = json.loads(text.strip())
            return result
        except Exception as e:
            # Fallback if AI fails
            return {
                "is_valid": False,
                "quality_score": 0,
                "issues": [f"AI validation failed: {str(e)}"],
                "corrected_question": question_text,
                "corrected_options": options,
                "correct_answer": correct_option,
                "duplicate": False,
                "difficulty": "Medium",
                "tags": ["Uncategorized"]
            }
