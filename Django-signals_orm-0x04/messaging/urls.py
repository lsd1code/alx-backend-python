from django.urls import path
from .views import deleter_user

urlpatterns = [
    path("user/<int:user_id>", deleter_user, name="delete_user"),
]
