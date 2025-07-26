from .models import User, Message, Conversation

from .serializers import *
from rest_framework import viewsets, permissions  
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404
from django.http import HttpRequest

from .permissions import UserAccessPermissions


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, UserAccessPermissions]

    def list(self, request):  # type:ignore        
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  # type:ignore
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):  # type:ignore
        serializer = ConversationSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  # type:ignore
        conversation = get_object_or_404(Conversation, pk=pk)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):  # type:ignore
        user = User.objects.first()
        conversation = Conversation(created_by=user)
        conversation.save()

        return Response({'data': True})


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [permissions.AllowAny]

    def list(self, request: HttpRequest, conversations_pk: str):
        serializer = MessageSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: HttpRequest, conversations_pk: str, pk=None):  # type:ignore
        message = get_object_or_404(Message, pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def create(self, request: HttpRequest, *args, **kwargs):  # type:ignore
        conversation = Conversation.objects.first()
        user = User.objects.first()

        message = Message(
            sender_id=user,
            message_body=request.data['message_body'],  # type:ignore
            conversation=conversation
        )

        message.save()
        return Response("create new message", status=201)
