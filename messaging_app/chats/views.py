from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse

from .models import User, Message, Conversation

from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response


class UserViewSet(viewsets.ViewSet):
    def list(self, req: HttpRequest):
        query_set = User.objects.all()
        serializer = UserSerializer(query_set, many=True)
        permission_classes = [AllowAny]

        return Response(serializer.data)


class ConversationViewSet:
    pass


class MessageViewSet:
    pass


def index(req: HttpRequest):
    conversations = Conversation.objects.all()
    serializer = ConversationSerializer(conversations, many=True)
    
    users = User.objects.all()
    # serializer = UserSerializer(users, many=True)

    return JsonResponse({'data': serializer.data})
