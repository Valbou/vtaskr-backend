import logging

from flask import Request

logger = logging.getLogger(__name__)

BEARER = "Bearer "


def get_bearer_token(request: Request) -> str | None:
    bearer = request.headers.get("Authorization")
    if bearer and bearer.startswith(BEARER):
        return bearer.replace(BEARER, "").strip()
    return bearer


def get_payload_token(request: Request) -> str | None:
    return request.get_json().get("token")


def get_querystring_token(request: Request) -> str | None:
    return request.args.to_dict().get("token")


def get_auth_token(request: Request) -> str | None:
    token = None
    methods = [get_bearer_token, get_payload_token, get_querystring_token]

    for method in methods:
        try:
            token = method(request=request)
            if token:
                break
        except Exception as e:
            logger.debug(f"Error in method {method.__name__}: {e}")

    return token


def get_ip(request) -> str:
    return (
        request.environ.get("HTTP_X_FORWARDED_FOR")
        or request.environ.get("REMOTE_ADDR")
        or "::1"
    )
