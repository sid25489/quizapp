import google.generativeai as genai
import numpy as np

class SimilarityEngine:
    def __init__(self):
        # We can use text-embedding-004
        self.model_name = 'models/text-embedding-004'

    def get_embedding(self, text):
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception:
            # Return dummy embedding if API fails
            return [0.0] * 768

    def cosine_similarity(self, vec1, vec2):
        if not vec1 or not vec2:
            return 0.0
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            return 0.0
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def is_duplicate(self, text1, text2, threshold=0.85):
        """
        AI semantic similarity check. Threshold: 85%
        """
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        similarity = self.cosine_similarity(emb1, emb2)
        return similarity >= threshold
