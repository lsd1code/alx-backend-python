from django.shortcuts import render
from django.http import HttpResponse

from .models import User, Notification, Message

def index(request):
    sender = User.objects.first()
    receiver = User.objects.last()
    
    m = Message(sender=sender, receiver=receiver, content="message content")
    m.save()

    return HttpResponse("hello test")
