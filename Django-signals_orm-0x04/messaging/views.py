from .models import User, Message

from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request


@api_view(['GET'])
def message_list(request: Request):
    messages = Message.objects.all()  # [21, 22, 23]
    return Response(f"Total Messages: {len(messages)}")


@api_view(['GET'])
def message(request: Request, message_id: int):
    message = Message.objects.filter(
        pk=message_id
    ).select_related().prefetch_related("replies").first()

    if not message:
        return Response("404 Message Not Found", status.HTTP_404_NOT_FOUND)

    replies = message.replies.all()  # type:ignore
    return Response(f"Message: {message.content}, replies: {len(replies)}")


@api_view(['POST'])
def create_message(request: Request):
    sender = get_object_or_404(
        User, pk=request.data.get("sender"))  # type:ignore
    receiver = get_object_or_404(
        User, pk=request.data.get("receiver"))  # type:ignore
    content = request.data.get("content")  # type:ignore

    if len(str(content)) < 1:
        return Response("Message content cannot be empty", status.HTTP_204_NO_CONTENT)

    Message.objects.create(sender=sender, receiver=receiver, content=content)
    return Response(f"Message created", status.HTTP_201_CREATED)


@api_view(['POST'])
def reply_message(request: Request, message_id: int):
    parent_message = get_object_or_404(Message, pk=message_id)
    reply_sender = get_object_or_404(
        User, pk=request.data["sender"])  # type:ignore
    reply_receiver = parent_message.sender

    Message.objects.create(
        # sender=reply_sender,
        sender=request.user,
        receiver=reply_receiver,
        parent_message=parent_message,
        content=request.data['content']  # type:ignore
    )

    return Response(f'Message {parent_message.content}', status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_user(request: Request, user_id: int):
    """
    Implement a post_delete signal on the User model to delete all messages, notifications, and message histories associated with the user.

    Ensure that foreign key constraints are respected during the deletion process by using CASCADE or custom signal logic.
    """
    user = get_object_or_404(User, pk=user_id)
    user.delete()

    return Response("User deleted successfully", status.HTTP_204_NO_CONTENT)
