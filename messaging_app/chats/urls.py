from django.urls import path, include
from .views import index, UserViewSet, ConversationViewSet, MessageViewSet

from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

router = routers.DefaultRouter()
router.register('conversation', ConversationViewSet, basename="conversation")
router.register('user', UserViewSet, basename="user")
router.register('message', MessageViewSet, basename="message")

nested_router = NestedDefaultRouter(router, 'conversation', lookup='conversation')
nested_router.register('message', MessageViewSet, basename='message')

urlpatterns = [
    path('', index, name="index"),
    path('api-auth', index, name="index"),
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]

# urlpatterns += router.urls
