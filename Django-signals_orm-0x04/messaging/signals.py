from .models import Notification, Message, MessageHistory

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


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
