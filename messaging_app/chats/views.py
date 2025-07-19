from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# from .models import User, Message

# Create your views here.
def index(req: HttpRequest):
  users = 1
  messages = 1
  
  
  return HttpResponse(f"Users:")