from django.urls import path, include
from .views import UserViewSet, ConversationViewSet, MessageViewSet

from rest_framework import routers  # type:ignore
from rest_framework_nested.routers import NestedDefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename="conversation")
router.register('users', UserViewSet, basename="user")

nested_router = NestedDefaultRouter(
    router, 'conversations', lookup='conversations')
nested_router.register('messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
