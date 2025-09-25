from django.urls import path
from .views import LoginView, CallbackView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path("login/", LoginView.as_view(), name="oidc_login"),
    path("callback/", CallbackView.as_view(), name="oidc_callback"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
   
]
