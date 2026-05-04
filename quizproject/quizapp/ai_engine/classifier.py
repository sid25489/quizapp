import json
import google.generativeai as genai

class AIClassifier:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def classify(self, question_text):
        """
        Standalone method to classify difficulty and generate tags.
        """
        prompt = f"""
        Analyze the following educational question:
        "{question_text}"
        
        Tasks:
        1. Classify difficulty as 'Easy', 'Medium', or 'Hard'.
        2. Generate 3-5 relevant tags.
        
        Respond ONLY with a JSON object:
        {{
            "difficulty": "Medium",
            "tags": ["tag1", "tag2"]
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            return json.loads(text.strip())
        except Exception:
            return {"difficulty": "Medium", "tags": ["Uncategorized"]}
