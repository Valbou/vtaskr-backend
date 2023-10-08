from json import dumps
from typing import Any

from flask import Response

JSON_MIME_TYPE = "application/json"


class ResponseAPI:
    @classmethod
    def get_response(cls, data: Any, status: int, headers: dict | None = None):
        headers = headers or {}
        assert (  # nosec
            status < 400
        ), f"A status >= 400 is an error not a normal response, given: {status}"
        response_data = dumps(data) if status != 204 else ""
        return Response(
            response=response_data,
            status=status,
            headers=headers,
            mimetype=JSON_MIME_TYPE,
            content_type=JSON_MIME_TYPE,
        )

    @classmethod
    def get_error_response(cls, message: str, status: int, headers: dict | None = None):
        data = {"error": message, "status": status}
        headers = headers or {}
        return Response(
            response=dumps(data),
            status=status,
            headers=headers,
            mimetype=JSON_MIME_TYPE,
            content_type=JSON_MIME_TYPE,
        )


class ResponseService:
    def check_rate_limite(self):
        pass

    def check_user(self):
        pass
