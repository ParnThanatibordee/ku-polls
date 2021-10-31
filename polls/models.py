"""model for ku-polls."""

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question model that contain question_text, pub_date, and end_date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date end', default=timezone.now() + datetime.timedelta(days=1))

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

    @property
    def votes(self) -> int:
        count = Vote.objects.filter(choice=self).count()
        return count

    def __str__(self):
        """Display choice_text."""
        return self.choice_text


class Vote(models.Model):
    """Vote model."""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote by {self.user.username} for {self.choice.choice_text}"