from django.urls import path, include
from .views import UserViewSet, ConversationViewSet, MessageViewSet

from rest_framework import routers # type:ignore
from rest_framework_nested.routers import NestedDefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename="conversation") #type:ignore
router.register('users', UserViewSet, basename="user") #type:ignore
router.register('messages', MessageViewSet, basename="messages") #type:ignore

# nested router
nested_router = NestedDefaultRouter(router, 'conversations', lookup='conversations')
nested_router.register('messages', MessageViewSet, basename='messages') #type:ignore



urlpatterns = [
    path('', include(router.urls)), #type:ignore
    path('', include(nested_router.urls)), #type:ignore
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
