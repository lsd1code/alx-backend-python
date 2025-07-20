from django.db import models
from django.contrib.auth.models import AbstractBaseUser

import uuid


class RoleChoices(models.TextChoices):
    GUEST = "guest"
    HOST = "host"
    ADMIN = "admin"


class User(AbstractBaseUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=11, null=False)
    role = models.CharField(
        max_length=10, choices=RoleChoices, default=RoleChoices.GUEST)
    creates_at = models.DateField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return f'User {self.user_id}: {self.first_name.capitalize()} {self.last_name.capitalize()}'


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="conversation")
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'Conversation {self.conversation_id}'


class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="message")
    message_body = models.CharField(max_length=255, blank=False, null=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')
    sent_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.message_id}: {self.message_body}'
