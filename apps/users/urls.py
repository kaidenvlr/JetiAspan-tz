from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from django.urls import path
from .views import RegistrationView, LogoutView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='token_blacklist'),
]
