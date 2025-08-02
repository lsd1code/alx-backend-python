from django.db import models

from .models import Message


class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_unread_messages(self):
        pass
