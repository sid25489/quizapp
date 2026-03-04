"""Utility helpers for quizapp views."""


def can_access_attempt(attempt, request):
    """Check if the request has permission to access this quiz attempt."""
    if attempt.user and request.user.is_authenticated:
        return attempt.user == request.user
    if attempt.user is None:
        return (
            attempt.session_key
            and request.session.session_key == attempt.session_key
        )
    return False
