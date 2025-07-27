from .models import User, Message, Conversation
from .pagination import CustomPageNumberPagination

from .serializers import *
from rest_framework import viewsets, permissions, status  
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404
from django.http import HttpRequest

from .permissions import (UserAccessPermissions, IsParticipantOfConversation)


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def list(self, request):  # type:ignore
        user = request.user
        user_id = request.data["user_id"]
        qs = super().get_queryset().filter(created_by=user_id)        
        serializer = ConversationSerializer(qs, many=True)    
            
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
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def list(self, request: HttpRequest, conversations_pk: str):
        conversation = Conversation.objects.get(conversation_id=conversations_pk)
        user_id = request.data["user_id"]
        
        is_participant = conversation.participants_id.filter(user_id=user_id).exists()
        
        if not is_participant:
            return Response({"data": "You are not a participant of this conversation"}, status.HTTP_403_FORBIDDEN)
        
        qs = Message.objects.filter(sender_id=user_id)
        serializer = MessageSerializer(qs, many=True)
        
        return Response(serializer.data)

    def retrieve(self, request: HttpRequest, conversations_pk: str, pk=None):  # type:ignore
        message = get_object_or_404(Message, pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def create(self, request: HttpRequest, *args, **kwargs):  # type:ignore
        conversation = Conversation.objects.first()
        user = User.objects.get(user_id=request.data["sender_id"])

        message = Message(
            sender_id=user,
            message_body=request.data['message_body'],  # type:ignore
            conversation=conversation
        )
        
        conversation.participants_id.add(user)
        message.save()
        
        return Response("create new message", status=201)
