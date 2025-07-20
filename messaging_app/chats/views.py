from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse

from .models import User, Message, Conversation

from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response


class UserViewSet:
    def list(self, req: HttpRequest):
        query_set = User.objects.all()
        serializer = UserSerializer(query_set, many=True)

        return Response(serializer.data)


class ConversationViewSet:
    pass


class MessageViewSet:
    pass


def index(req: HttpRequest):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return JsonResponse({'data': serializer.data})
