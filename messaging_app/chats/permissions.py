from rest_framework import permissions

class UserAccessPermissions(permissions.BasePermission):
  def has_permission(self, request, view):
    user = request.user
    return user.is_authenticated


class IsParticipantOfConversation(permissions.BasePermission):
  def has_permission(self):
    user = request.user
    
    if not user.is_authenticated:
      return False
    
    # todo: check if the user is a participant
    
    return True