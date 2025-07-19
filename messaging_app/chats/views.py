from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import User, Message, Conversation

# Create your views here.
def index(req: HttpRequest):
  users = User.objects.all()
  
  u1 = users.first()
  u2 = users.first()
  
  m1 = Message(sender_id=u1, message_body="This is message 1")
  m2 = Message(sender_id=u2, message_body="This is message 1")
  
  convo = Conversation()
  convo.save()
  
  
  return HttpResponse(f"Users:")