from django.urls import path
from .views import index, UserViewSet, ConversationViewSet, MessageViewSet

from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', index, name="index"),
    # path('users', UserViewSet.as_view(), name='users')
]

router = DefaultRouter() 
router.register('conversation', ConversationViewSet, basename="conversations")
router.register('user', UserViewSet, basename="user")
router.register('message', MessageViewSet, basename="message")

urlpatterns += router.urls
