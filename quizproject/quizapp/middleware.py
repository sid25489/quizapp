"""Middleware for quizapp."""

_quizzes_loaded = False


class LoadPracticeQuizzesMiddleware:
    """
    Load practice quizzes on first request if the database is empty.
    Ensures quizzes are available when the project starts (runserver, gunicorn)
    without requiring a manual migrate step for the data.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global _quizzes_loaded
        if not _quizzes_loaded:
            _quizzes_loaded = True
            try:
                from quizapp.loaders import load_practice_quizzes
                load_practice_quizzes()
            except Exception:
                pass
        return self.get_response(request)
