from django.urls import path, include
from .views import index, UserViewSet, ConversationViewSet, MessageViewSet

from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', index, name="index"),
    # path('users', UserViewSet.as_view(), name='users')
]

routers = DefaultRouter()
routers.register('conversation', ConversationViewSet, basename="conversations")
routers.register('user', UserViewSet, basename="user")
routers.register('message', MessageViewSet, basename="message")

urlpatterns += router.urls
