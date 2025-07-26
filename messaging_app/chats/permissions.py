from rest_framework import permissions

class UserAccessPermissions(permissions.BasePermission):
  def has_permission(self, request, view):
    user = request.user
    
    return user.is_authenticated


class IsParticipantOfConversation(permissions.BasePermission):
  def has_permission(self):
    pass