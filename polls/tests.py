from django.test import TestCase
from django.utils import timezone
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
        now = timezone.now()
        q = Question.objects.create(question_text="now", pub_date=now)
        self.assertTrue(q.was_published_recently())

    def test_was_published_recently_exactly_24h_old(self):
        boundary = timezone.now() - datetime.timedelta(days=1)
        q = Question.objects.create(question_text="boundary", pub_date=boundary)
        # Your implementation uses >= lower bound, so boundary counts as recent.
        self.assertTrue(q.was_published_recently())

    # --- __str__ representation ---
    def test_question_str(self):
        q = Question.objects.create(question_text="Who?", pub_date=timezone.now())
        self.assertEqual(str(q), "Who?")


class ChoiceModelTests(TestCase):
    def test_choice_str_and_default_votes(self):
        q = Question.objects.create(question_text="Pick one", pub_date=timezone.now())
        c = Choice.objects.create(question=q, choice_text="A")
        # __str__ should be the choice text
        self.assertEqual(str(c), "A")
        # default votes should be 0
        self.assertEqual(c.votes, 0)
