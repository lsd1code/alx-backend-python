from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UnreadMessagesManager


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

    def __str__(self) -> str:
        return f"{self.username}"


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver_messages"
    )
    parent_message = models.ForeignKey(
        'self', on_delete=models.SET_NULL, related_name="replies", blank=True, null=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    unread = models.BooleanField(default=True)

    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self) -> str:
        return f'Content: {self.content}'


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="messages")

    def __str__(self) -> str:
        return f'Notification for {self.user.username}'


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history")
    edited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="edited_messages")
    edited_at = models.DateTimeField(auto_now=True)
    old_content = models.TextField()
