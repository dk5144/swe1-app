from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch
import datetime

from polls.models import Question, Choice


class QuestionModelTests(TestCase):
    # --- was_published_recently edge cases ---

    def test_was_published_recently_future(self):
        future = timezone.now() + datetime.timedelta(days=1)
        q = Question.objects.create(question_text="f", pub_date=future)
        self.assertFalse(q.was_published_recently())

    def test_was_published_recently_old(self):
        old = timezone.now() - datetime.timedelta(days=1, seconds=1)
        q = Question.objects.create(question_text="o", pub_date=old)
        self.assertFalse(q.was_published_recently())

    def test_was_published_recently_recent(self):
        recent = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        q = Question.objects.create(question_text="r", pub_date=recent)
        self.assertTrue(q.was_published_recently())

    def test_was_published_recently_exact_now(self):
        fixed_now = timezone.now().replace(microsecond=0)
        with patch("polls.models.timezone.now", return_value=fixed_now):
            q = Question.objects.create(question_text="now", pub_date=fixed_now)
            self.assertTrue(q.was_published_recently())

    def test_was_published_recently_exactly_24h_old(self):
        fixed_now = timezone.now().replace(microsecond=0)
        boundary = (fixed_now - datetime.timedelta(days=1)).replace(microsecond=0)
        with patch("polls.models.timezone.now", return_value=fixed_now):
            q = Question.objects.create(question_text="boundary", pub_date=boundary)
            self.assertTrue(q.was_published_recently())

    # --- __str__ representation ---

    def test_question_str(self):
        q = Question.objects.create(question_text="Who?", pub_date=timezone.now())
        self.assertEqual(str(q), "Who?")


class ChoiceModelTests(TestCase):
    def test_choice_str_and_default_votes(self):
        q = Question.objects.create(question_text="Pick one", pub_date=timezone.now())
        c = Choice.objects.create(question=q, choice_text="A")
        self.assertEqual(str(c), "A")  # __str__
        self.assertEqual(c.votes, 0)  # default votes
