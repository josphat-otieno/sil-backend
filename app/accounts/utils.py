
# yourproject/auth/utils.py
import time
import requests
from django.conf import settings
from jwt import PyJWKClient, decode as jwt_decode, InvalidTokenError, ExpiredSignatureError

_cache = {
    "discovery": {"value": None, "expires": 0},
    "jwks_client": {"value": None, "expires": 0},
}

def get_discovery():
    """Fetch and cache discovery document."""
    now = time.time()
    if _cache["discovery"]["value"] and _cache["discovery"]["expires"] > now:
        return _cache["discovery"]["value"]
    r = requests.get(settings.OIDC_DISCOVERY_URL, timeout=5)
    r.raise_for_status()
    doc = r.json()
    _cache["discovery"]["value"] = doc
    _cache["discovery"]["expires"] = now + settings.OIDC_CACHE_TTL
    return doc

def get_jwks_client():
    """Return a PyJWKClient instance for the provider's JWKS URI (cached)."""
    now = time.time()
    if _cache["jwks_client"]["value"] and _cache["jwks_client"]["expires"] > now:
        return _cache["jwks_client"]["value"]
    discovery = get_discovery()
    jwks_uri = discovery.get("jwks_uri")
    if not jwks_uri:
        raise RuntimeError("jwks_uri not found in discovery document")
    client = PyJWKClient(jwks_uri)
    _cache["jwks_client"]["value"] = client
    _cache["jwks_client"]["expires"] = now + settings.OIDC_CACHE_TTL
    return client

def verify_token(token: str, audience: str = None, issuer: str = None):
    """
    Verify a JWT (access_token or id_token) using JWKS.
    Returns the decoded claims (dict) on success.
    Raises InvalidTokenError/ExpiredSignatureError on failure.
    """
    audience = audience or settings.OIDC_CLIENT_ID
    issuer = issuer or settings.OIDC_ISSUER
    jwks_client = get_jwks_client()
    signing_key = jwks_client.get_signing_key_from_jwt(token).key
    try:
        claims = jwt_decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=audience,
            issuer=issuer,
            options={"verify_at_hash": False},
            leeway=10,  # allow 10 seconds clock skew
            
        )
        return claims
    except ExpiredSignatureError:
        raise
    except InvalidTokenError:
        raise

