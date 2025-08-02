from .models import Notification, Message, MessageHistory, User

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete


"""
Implement a post_delete signal on the User model to delete all messages, notifications, and message histories associated with the user.

Ensure that foreign key constraints are respected during the deletion process by using CASCADE or custom signal logic.
"""


@receiver(post_delete, sender=User, dispatch_uid="delete_user")
def delete_user_related_data(sender, instance, **kwargs):
    print("delete user signal fired")


@receiver(pre_save, sender=Message, dispatch_uid="update_message")
def log_and_save_old_content_before_edit(sender, instance, **kwargs):
    """
    Signal that log when a user edits a message and save the old content before the edit
    """
    exists = Message.objects.filter(pk=instance.pk).exists()

    if exists:
        message = Message.objects.get(pk=instance.pk)

        if message.content != instance.content:
            MessageHistory.objects.create(
                message=message,
                old_content=message.content,
                edited_by=message.sender
            )
            print("message updated")


@receiver(post_save, sender=Message, dispatch_uid="create_new_notification")
def send_notification_when_message_is_created(sender, instance, created, **kwargs):
    """
    Signal that listens for new messages and automatically creates a notification for the receiver user
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
