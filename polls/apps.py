"""Application."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Configure poll."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
