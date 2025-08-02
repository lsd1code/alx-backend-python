from django.shortcuts import render
from django.http import HttpResponse

from .models import User, Notification, Message


def index(request):
    # m = Message.objects.all().last()
    # print(m.history.all())
    # m.content = "new update here"
    # m.save()

    return HttpResponse("hello test")
