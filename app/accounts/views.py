# yourproject/auth/views.py
from django.views import View
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.contrib.auth import get_user_model, login as django_login
from .models import Customer
from .utils import get_discovery, verify_token
import requests

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from urllib.parse import urlencode


class LoginView(View):
    def get(self, request, *args, **kwargs):
        discovery = get_discovery()
        auth_url = discovery["authorization_endpoint"]
        params = {
            "client_id": settings.OIDC_CLIENT_ID,
            "response_type": "code",
            "scope": "openid email profile phone",
            "redirect_uri": settings.OIDC_REDIRECT_URI,
            "prompt": "select_account",
            "access_type": "offline",
            "state": "state-xyz",  # TODO: implement CSRF/state
        }
        from urllib.parse import urlencode
        return redirect(f"{auth_url}?{urlencode(params)}")


class CallbackView(View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            return HttpResponseBadRequest("Missing code parameter")

        discovery = get_discovery()
        token_url = discovery["token_endpoint"]
        data = {
            "code": code,
            "client_id": settings.OIDC_CLIENT_ID,
            "client_secret": settings.OIDC_CLIENT_SECRET,
            "redirect_uri": settings.OIDC_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        r = requests.post(token_url, data=data, timeout=10)
        r.raise_for_status()
        token_resp = r.json()
        id_token = token_resp.get("id_token")
        access_token = token_resp.get("access_token")

        # Verify id_token
        claims = verify_token(id_token, audience=settings.OIDC_CLIENT_ID, issuer=settings.OIDC_ISSUER)

        # Map to User + Customer
        User = get_user_model()
        sub = claims.get("sub")
        email = claims.get("email")
        phone = claims.get("phone_number")
        username = email or sub

        user, _ = User.objects.get_or_create(username=username, defaults={"email": email or ""})
        customer, _ = Customer.objects.get_or_create(
            sub=sub, defaults={"user": user, "email": email or "", "phone": phone or ""}
        )
        # keep info updated
        if not customer.user:
            customer.user = user
        if email and not customer.email:
            customer.email = email
        if phone and not customer.phone:
            customer.phone = phone
        customer.save()

        django_login(request, user)

        return JsonResponse({
            "message": "Logged in",
            "user": {"username": user.username, "email": user.email},
            "tokens": {"id_token": id_token, "access_token": access_token},
        })





