from django.urls import path
from .views import delete_user

urlpatterns = [
    path("user/<int:user_id>", delete_user, name="delete_user"),
]
