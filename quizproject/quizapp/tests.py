from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Quiz, Question, Choice, QuizAttempt, UserAnswer


def create_quiz_with_questions(title="Test Quiz", num_questions=2, points_per_question=1):
    """Helper: Create a quiz with questions and choices."""
    quiz = Quiz.objects.create(title=title, description="Test", is_active=True)
    for i in range(num_questions):
        q = Question.objects.create(quiz=quiz, text=f"Q{i+1}", order=i, points=points_per_question)
        Choice.objects.create(question=q, text="Correct", is_correct=True)
        Choice.objects.create(question=q, text="Wrong", is_correct=False)
    return quiz


class QuizModelTests(TestCase):
    def test_get_questions_count(self):
        quiz = create_quiz_with_questions(num_questions=3)
        self.assertEqual(quiz.get_questions_count(), 3)

    def test_get_total_score(self):
        quiz = create_quiz_with_questions(num_questions=2, points_per_question=5)
        self.assertEqual(quiz.get_total_score(), 10)

    def test_str(self):
        quiz = Quiz.objects.create(title="My Quiz", is_active=True)
        self.assertIn("My Quiz", str(quiz))


class QuestionModelTests(TestCase):
    def test_get_correct_choice(self):
        quiz = create_quiz_with_questions(num_questions=1)
        q = quiz.questions.first()
        correct = q.get_correct_choice()
        self.assertIsNotNone(correct)
        self.assertTrue(correct.is_correct)


class ChoiceModelTests(TestCase):
    def test_choice_belongs_to_question(self):
        quiz = create_quiz_with_questions(num_questions=1)
        q = quiz.questions.first()
        choices = list(q.choices.all())
        self.assertEqual(len(choices), 2)


class QuizAttemptModelTests(TestCase):
    def setUp(self):
        self.quiz = create_quiz_with_questions(num_questions=2, points_per_question=2)

    def test_calculate_score_all_correct(self):
        attempt = QuizAttempt.objects.create(quiz=self.quiz, total_score=4)
        q1, q2 = list(self.quiz.questions.all())
        c1 = q1.choices.filter(is_correct=True).first()
        c2 = q2.choices.filter(is_correct=True).first()
        UserAnswer.objects.create(attempt=attempt, question=q1, selected_choice=c1)
        UserAnswer.objects.create(attempt=attempt, question=q2, selected_choice=c2)
        attempt.calculate_score()
        self.assertEqual(attempt.score, 4)
        self.assertEqual(attempt.total_score, 4)

    def test_calculate_score_partial(self):
        attempt = QuizAttempt.objects.create(quiz=self.quiz, total_score=4)
        q1, q2 = list(self.quiz.questions.all())
        c1_correct = q1.choices.filter(is_correct=True).first()
        c2_wrong = q2.choices.filter(is_correct=False).first()
        UserAnswer.objects.create(attempt=attempt, question=q1, selected_choice=c1_correct)
        UserAnswer.objects.create(attempt=attempt, question=q2, selected_choice=c2_wrong)
        attempt.calculate_score()
        self.assertEqual(attempt.score, 2)
        self.assertEqual(attempt.total_score, 4)

    def test_get_percentage(self):
        attempt = QuizAttempt.objects.create(quiz=self.quiz, score=2, total_score=4)
        self.assertEqual(attempt.get_percentage(), 50.0)

    def test_get_percentage_zero_total(self):
        attempt = QuizAttempt.objects.create(quiz=self.quiz, score=0, total_score=0)
        self.assertEqual(attempt.get_percentage(), 0)


class UserAnswerModelTests(TestCase):
    def test_is_correct_true(self):
        quiz = create_quiz_with_questions(num_questions=1)
        attempt = QuizAttempt.objects.create(quiz=quiz, total_score=1)
        q = quiz.questions.first()
        correct = q.choices.filter(is_correct=True).first()
        answer = UserAnswer.objects.create(attempt=attempt, question=q, selected_choice=correct)
        self.assertTrue(answer.is_correct())

    def test_is_correct_false(self):
        quiz = create_quiz_with_questions(num_questions=1)
        attempt = QuizAttempt.objects.create(quiz=quiz, total_score=1)
        q = quiz.questions.first()
        wrong = q.choices.filter(is_correct=False).first()
        answer = UserAnswer.objects.create(attempt=attempt, question=q, selected_choice=wrong)
        self.assertFalse(answer.is_correct())


class HomeViewTests(TestCase):
    def test_home_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_shows_quiz_count(self):
        create_quiz_with_questions()
        response = self.client.get(reverse('home'))
        self.assertContains(response, '1')


class QuizListViewTests(TestCase):
    def test_quiz_list_returns_200(self):
        response = self.client.get(reverse('quiz_list'))
        self.assertEqual(response.status_code, 200)

    def test_quiz_list_shows_quizzes(self):
        quiz = create_quiz_with_questions(title="Python Quiz")
        response = self.client.get(reverse('quiz_list'))
        self.assertContains(response, "Python Quiz")


class QuizDetailViewTests(TestCase):
    def test_quiz_detail_returns_200(self):
        quiz = create_quiz_with_questions()
        response = self.client.get(reverse('quiz_detail', args=[quiz.id]))
        self.assertEqual(response.status_code, 200)

    def test_quiz_detail_404_inactive(self):
        quiz = create_quiz_with_questions()
        quiz.is_active = False
        quiz.save()
        response = self.client.get(reverse('quiz_detail', args=[quiz.id]))
        self.assertEqual(response.status_code, 404)


class StartQuizViewTests(TestCase):
    def test_start_quiz_redirects_to_take_quiz(self):
        quiz = create_quiz_with_questions()
        response = self.client.get(reverse('start_quiz', args=[quiz.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/attempt/', response.url)
        self.assertEqual(QuizAttempt.objects.count(), 1)

    def test_start_quiz_empty_quiz_redirects_back(self):
        quiz = Quiz.objects.create(title="Empty", is_active=True)
        response = self.client.get(reverse('start_quiz', args=[quiz.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(f'/quiz/{quiz.id}/', response.url)
        self.assertEqual(QuizAttempt.objects.count(), 0)


class TakeQuizViewTests(TestCase):
    def setUp(self):
        self.quiz = create_quiz_with_questions(num_questions=2)
        self.client = Client()
        self.client.get('/')  # ensure session exists

    def test_take_quiz_returns_200(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key=self.client.session.session_key,
            total_score=self.quiz.get_total_score()
        )
        response = self.client.get(reverse('take_quiz', args=[attempt.id]))
        self.assertEqual(response.status_code, 200)

    def test_take_quiz_completed_redirects_to_result(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key=self.client.session.session_key,
            total_score=2,
            is_completed=True
        )
        response = self.client.get(reverse('take_quiz', args=[attempt.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('result', response.url)

    def test_take_quiz_anonymous_wrong_session_redirects(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key="wrong-session-key",
            total_score=2
        )
        response = self.client.get(reverse('take_quiz', args=[attempt.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))


class SubmitQuizViewTests(TestCase):
    def setUp(self):
        self.quiz = create_quiz_with_questions(num_questions=2, points_per_question=1)
        self.client = Client()
        self.client.get('/')

    def test_submit_quiz_scores_correctly(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key=self.client.session.session_key,
            total_score=2
        )
        q1, q2 = list(self.quiz.questions.all())
        c1 = q1.choices.filter(is_correct=True).first()
        c2 = q2.choices.filter(is_correct=True).first()
        data = {
            'csrfmiddlewaretoken': 'test',
            f'question_{q1.id}': str(c1.id),
            f'question_{q2.id}': str(c2.id),
        }
        response = self.client.post(reverse('submit_quiz', args=[attempt.id]), data)
        self.assertEqual(response.status_code, 302)
        attempt.refresh_from_db()
        self.assertTrue(attempt.is_completed)
        self.assertEqual(attempt.score, 2)

    def test_submit_quiz_anonymous_wrong_session_denied(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key="wrong-key",
            total_score=2
        )
        response = self.client.post(reverse('submit_quiz', args=[attempt.id]), {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))


class QuizResultViewTests(TestCase):
    def setUp(self):
        self.quiz = create_quiz_with_questions()
        self.client = Client()
        self.client.get('/')

    def test_quiz_result_incomplete_redirects_to_take(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key=self.client.session.session_key,
            total_score=2
        )
        response = self.client.get(reverse('quiz_result', args=[attempt.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('attempt', response.url)

    def test_quiz_result_completed_returns_200(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key=self.client.session.session_key,
            total_score=2,
            score=1,
            is_completed=True
        )
        response = self.client.get(reverse('quiz_result', args=[attempt.id]))
        self.assertEqual(response.status_code, 200)

    def test_quiz_result_anonymous_wrong_session_denied(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key="wrong-key",
            total_score=2,
            is_completed=True
        )
        response = self.client.get(reverse('quiz_result', args=[attempt.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))


class LeaderboardViewTests(TestCase):
    def test_leaderboard_returns_200(self):
        quiz = create_quiz_with_questions()
        response = self.client.get(reverse('leaderboard', args=[quiz.id]))
        self.assertEqual(response.status_code, 200)


class MyAttemptsViewTests(TestCase):
    def test_my_attempts_redirects_anonymous(self):
        response = self.client.get(reverse('my_attempts'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_my_attempts_returns_200_when_logged_in(self):
        user = User.objects.create_user('testuser', 'test@example.com', 'pass')
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('my_attempts'))
        self.assertEqual(response.status_code, 200)


class SaveAnswerViewTests(TestCase):
    def setUp(self):
        self.quiz = create_quiz_with_questions()
        self.client = Client()
        self.client.get('/')
        # Ensure session has a key (lazy creation)
        if not self.client.session.session_key:
            self.client.session.create()
        self.client.session.save()

    def test_save_answer_success_authenticated(self):
        user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        self.client.login(username='testuser', password='pass')
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            user=user,
            total_score=2
        )
        q = self.quiz.questions.first()
        c = q.choices.first()
        response = self.client.post(
            reverse('save_answer', args=[attempt.id]),
            {'question_id': str(q.id), 'choice_id': str(c.id)}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(UserAnswer.objects.filter(attempt=attempt).count(), 1)

    def test_save_answer_success_anonymous(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key=self.client.session.session_key,
            total_score=2
        )
        q = self.quiz.questions.first()
        c = q.choices.first()
        response = self.client.post(
            reverse('save_answer', args=[attempt.id]),
            {'question_id': str(q.id), 'choice_id': str(c.id)}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

    def test_save_answer_anonymous_wrong_session_403(self):
        attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            session_key="wrong-key",
            total_score=2
        )
        q = self.quiz.questions.first()
        c = q.choices.first()
        response = self.client.post(
            reverse('save_answer', args=[attempt.id]),
            {'question_id': q.id, 'choice_id': c.id}
        )
        self.assertEqual(response.status_code, 403)


class APIViewTests(TestCase):
    def test_quiz_api_list_returns_json(self):
        create_quiz_with_questions(title="API Quiz")
        response = self.client.get(reverse('quiz_api_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('quizzes', data)
        self.assertGreaterEqual(len(data['quizzes']), 1)
        titles = [q['title'] for q in data['quizzes']]
        self.assertIn("API Quiz", titles)

    def test_quiz_api_detail_returns_json(self):
        quiz = create_quiz_with_questions(title="Detail Quiz")
        response = self.client.get(reverse('quiz_api_detail', args=[quiz.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], "Detail Quiz")
        self.assertIn('questions', data)


class IntegrationQuizFlowTests(TestCase):
    """Full quiz flow: start -> take -> submit -> result."""

    def test_anonymous_full_quiz_flow(self):
        client = Client()
        client.get('/')  # ensure session
        quiz = create_quiz_with_questions(num_questions=2, points_per_question=2)

        # Start
        r = client.get(reverse('start_quiz', args=[quiz.id]))
        self.assertEqual(r.status_code, 302)
        attempt = QuizAttempt.objects.get(quiz=quiz)
        self.assertEqual(attempt.session_key, client.session.session_key)

        # Take (view questions)
        r = client.get(reverse('take_quiz', args=[attempt.id]))
        self.assertEqual(r.status_code, 200)

        # Submit with answers
        q1, q2 = list(quiz.questions.all())
        c1 = q1.choices.filter(is_correct=True).first()
        c2 = q2.choices.filter(is_correct=False).first()
        data = {
            f'question_{q1.id}': str(c1.id),
            f'question_{q2.id}': str(c2.id),
        }
        r = client.post(reverse('submit_quiz', args=[attempt.id]), data)
        self.assertEqual(r.status_code, 302)
        attempt.refresh_from_db()
        self.assertTrue(attempt.is_completed)
        self.assertEqual(attempt.score, 2)
        self.assertEqual(attempt.total_score, 4)

        # Result
        r = client.get(reverse('quiz_result', args=[attempt.id]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "2")
        self.assertContains(r, "4")
