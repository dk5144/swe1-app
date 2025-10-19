from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from django.test import TestCase
from polls.models import Question

class QuestionModelTests(TestCase):
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
