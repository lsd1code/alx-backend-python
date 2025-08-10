<<<<<<< HEAD
<<<<<<< HEAD
from django.db import models
from django.shortcuts import get_object_or_404


class UnreadMessagesManager(models.Manager):
    def unread(self):
        return self.get_queryset().filter(unread=True)

    def unread_for_user(self, user_id):
        return self.get_queryset().filter(sender__id=2)
=======
=======
>>>>>>> e696047 (FEAT: setup a docker environment)
from django.db import models
from django.shortcuts import get_object_or_404

# from .models import User


class UnreadMessagesManager(models.Manager):
    def unread(self):
        return self.get_queryset().filter(unread=True)

    def unread_for_user(self, user_id):
        return self.get_queryset().filter(sender=user_id)
<<<<<<< HEAD
>>>>>>> e696047 (FEAT: setup a docker environment)
=======
>>>>>>> e696047 (FEAT: setup a docker environment)
