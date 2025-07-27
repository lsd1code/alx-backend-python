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

        # todo: update and delete message in a conversation
        if request.method == "DELETE":
            #! check if the user is the sender of the message
            pass

        if request.method == "PUT":
            #! check if the user is the sender of the message
            pass

        if request.method == "PATCH":
            #! check if the user is the sender of the message
            pass

        return True
