from .models import Notification, Message, User

from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Message, dispatch_uid="create_new_notification")
def send_notification_when_message_is_created(sender, instance, created, **kwargs):
    """
    Signal that listens for new messages and automatically creates a notification for the receiver user
    """

    if created:
        user = instance.receiver

        n = Notification(user=user, message=instance)
        n.save()

        print("create new notification")
