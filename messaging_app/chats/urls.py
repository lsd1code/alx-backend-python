from django.urls import path
from .views import index, UserViewSet

from rest_framework.routers import DefaultRouter

urlpatterns = [
  path('', index, name="index"),
  # path('users', UserViewSet.as_view(), name='users')
]

router = DefaultRouter()
router.register('users', UserViewSet, basename="users")

urlpatterns += router.urls
