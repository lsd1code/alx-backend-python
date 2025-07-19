from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import user, message

# Create your views here.
def index(req: HttpRequest):
  users = user.objects.all()
  messages = message.objects.all()
  
  print(users)
  
  return HttpResponse(f"Users: {len(users)} - Messages: {len(messages)}")