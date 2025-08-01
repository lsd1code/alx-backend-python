from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="messaging_user_set",  # Add a unique related_name
        related_query_name="messaging_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="messaging_user_permissions_set",  # Add a unique related_name
        related_query_name="messaging_user_permission",
    )


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender_messages")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_created=True)

    def __str__(self) -> str:
        return f'From {self.sender.username} to {self.receiver.username}'


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="messages")
