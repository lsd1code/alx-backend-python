from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import User, Notification, Message
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request


@api_view(['DELETE'])
def delete_user(request: Request, user_id: int):
    """
    Implement a post_delete signal on the User model to delete all messages, notifications, and message histories associated with the user.

    Ensure that foreign key constraints are respected during the deletion process by using CASCADE or custom signal logic.
    """
    user = get_object_or_404(User, pk=user_id)
    user.delete()

    return Response("User deleted successfully")
