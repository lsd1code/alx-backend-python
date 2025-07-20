from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse

from .models import User, Message, Conversation

from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # return Response(serializer.data)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.AllowAny]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]


def index(req: HttpRequest):
    conversations = Conversation.objects.all()
    serializer = ConversationSerializer(conversations, many=True)

    users = User.objects.all()
    # serializer = UserSerializer(users, many=True)

    return JsonResponse({'data': serializer.data})
