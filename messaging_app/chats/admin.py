from django.contrib import admin
from .models import user, message

# Register your models here.
admin.site.register(user)
admin.site.register(message)