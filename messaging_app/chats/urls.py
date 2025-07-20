from django.urls import path, include
from .views import index, UserViewSet, ConversationViewSet, MessageViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register('conversation', ConversationViewSet, basename="conversations")
router.register('user', UserViewSet, basename="user")
router.register('message', MessageViewSet, basename="message")


urlpatterns = [
    path('', index, name="index"),
    # path('users', UserViewSet.as_view(), name='users')
].append(router.urls)


