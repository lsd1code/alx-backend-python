from django.urls import path
from .views import (
    delete_user,
    message,
    create_message,
    message_list,
    reply_message,
    unread_message_list
)

urlpatterns = [
    path("users/<int:user_id>", delete_user, name="delete_user"),
    path("messages/", unread_message_list, name="message_list"),
    path("messages/create", create_message, name="create_message"),
    path("messages/<int:message_id>", message, name="message"),
    path(
        "messages/<int:message_id>/reply", reply_message, name="reply_message"
    ),
]
