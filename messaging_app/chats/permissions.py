from rest_framework import permissions

class UserAccessPermissions(permissions.BasePermission):
  def has_permission(self, request, view):
    print("user access permissions class")
    print(request.method)


class IsParticipantOfConversation(permissions.BasePermission):
  def has_permission(self):
    pass