from rest_framework import permissions
from .models import Conversation

class UserAccessPermissions(permissions.BasePermission):
  def has_permission(self, request, view):
    user = request.user
    return user.is_authenticated


class IsParticipantOfConversation(permissions.BasePermission):
  def has_permission(self, request, view):
    user = request.user
    
    if not user.is_authenticated:
      return False
    
    if request.method == "DELETE":
      pass
    
    if request.method == "PUT":
      pass
    
    if request.method == "PATCH":
      pass
        
    return True