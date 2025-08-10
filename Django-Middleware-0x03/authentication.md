# Auth with JWT

- package

```shell
# installation
pip install djangorestframework-simplejwt
```

- project configuration

```python
# settings.py
REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    "rest_framework.authentication.SessionAuthentication"
  )
}


# urls.py (app) level
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ...
]

send requests to the first url path to get access and refresh tokens
for admin users = [username, password]
```