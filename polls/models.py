"""model for ku-polls."""

import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Question model that contain question_text, pub_date, and end_date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('ending date')

    def was_published_recently(self):
        """Check that the question was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check that the question was already published."""
        now = timezone.now()
        if now >= self.pub_date:
            return True
        return False

    def can_vote(self):
        """Check that the question can vote."""
        now = timezone.now()
        return self.end_date >= now >= self.pub_date

    def __str__(self):
        """Display question_text."""
        return self.question_text


class Choice(models.Model):
    """Choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Display choice_text."""
        return self.choice_text
