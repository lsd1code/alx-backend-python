from django.shortcuts import render
from django.http import HttpResponse

from .models import User, Notification, Message


def index(request):
    return HttpResponse("hello test")
