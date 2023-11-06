from flask import Request

BEARER = "Bearer "


def get_bearer_token(request: Request) -> str | None:
    bearer = request.headers.get("Authorization")
    if bearer and bearer.startswith(BEARER):
        return bearer.replace(BEARER, "").strip()
    return bearer


def get_ip(request) -> str:
    return (
        request.environ.get("HTTP_X_FORWARDED_FOR")
        or request.environ.get("REMOTE_ADDR")
        or "::1"
    )
