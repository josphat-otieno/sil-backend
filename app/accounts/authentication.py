
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header
from django.conf import settings
from .utils import verify_token

User = get_user_model()

class OIDCAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b"bearer":
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Invalid Authorization header. No credentials provided.")
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed("Invalid Authorization header. Token string should not contain spaces.")

        token = auth[1].decode("utf-8")
        try:
            claims = verify_token(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Token verification failed: {str(e)}")

        # Prefer email for username mapping
        email = claims.get("email")
        sub = claims.get("sub")
        if not sub:
            raise exceptions.AuthenticationFailed("Token missing 'sub' claim")

        user = None
        if email:
            user, created = User.objects.get_or_create(username=email, defaults={"email": email})
        else:
            # fallback to sub-based username
            user, created = User.objects.get_or_create(username=sub)

        return (user, claims)
