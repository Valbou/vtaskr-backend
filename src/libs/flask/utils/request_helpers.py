from flask import Request

BEARER = "Bearer "


def get_bearer_token(request: Request) -> str | None:
    bearer = request.headers.get("Authorization")
    if bearer and bearer.startswith(BEARER):
        return bearer.replace(BEARER, "").strip()
    return bearer


def get_payload_token(request: Request) -> str | None:
    token = request.get_json().get("token")
    return token


def get_auth_token(request: Request) -> str | None:
    token = None
    methods = [get_bearer_token, get_payload_token]

    for method in methods:
        token = method(request=request)
        if token:
            break

    return token


def get_ip(request) -> str:
    return (
        request.environ.get("HTTP_X_FORWARDED_FOR")
        or request.environ.get("REMOTE_ADDR")
        or "::1"
    )
