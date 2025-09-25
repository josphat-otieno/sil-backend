from django.urls import path
from .views import LoginView, CallbackView,KeycloakLoginView,KeycloakCallbackView
urlpatterns=[
    path("login/", LoginView.as_view(), name="oidc_login"),
    path("callback/", CallbackView.as_view(), name="oidc_callback"),
    path("keycloak/login/", KeycloakLoginView.as_view(), name="keycloak_login"),
    path("keycloak/callback/", KeycloakCallbackView.as_view(), name="keycloak_callback"),
]
