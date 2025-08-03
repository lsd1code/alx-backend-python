from django.db import models
from django.shortcuts import get_object_or_404


class UnreadMessagesManager(models.Manager):
    def unread(self):
        return self.get_queryset().filter(unread=True)

    def unread_for_user(self, user_id):
        return self.get_queryset().filter(sender__id=2)
