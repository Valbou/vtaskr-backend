from json import dumps
from typing import Any

from flask import Response

JSON_MIME_TYPE = "application/json"


class ResponseAPI:
    @classmethod
    def get_response(
        cls, data: Any, status: int, headers: dict | None = None
    ) -> Response:
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
    def get_error_response(
        cls, message: str, status: int, headers: dict | None = None
    ) -> Response:
        data = {"error": message, "status": status}
        headers = headers or {}
        return Response(
            response=dumps(data),
            status=status,
            headers=headers,
            mimetype=JSON_MIME_TYPE,
            content_type=JSON_MIME_TYPE,
        )

    @classmethod
    def get_400_response(
        cls, message: str = "", headers: dict | None = None
    ) -> Response:
        message = message or "Bad request"
        return cls.get_error_response(message=message, status=400, headers=headers)

    @classmethod
    def get_401_response(
        cls, message: str = "", headers: dict | None = None
    ) -> Response:
        message = message or "Unauthorized"
        return cls.get_error_response(message=message, status=401, headers=headers)

    @classmethod
    def get_403_response(
        cls, message: str = "", headers: dict | None = None
    ) -> Response:
        message = message or "Forbidden"
        return cls.get_error_response(message=message, status=403, headers=headers)

    @classmethod
    def get_404_response(
        cls, message: str = "", headers: dict | None = None
    ) -> Response:
        message = message or "Not found"
        return cls.get_error_response(message=message, status=404, headers=headers)

    @classmethod
    def get_405_response(
        cls, message: str = "", headers: dict | None = None
    ) -> Response:
        message = message or "Method not allowed"
        return cls.get_error_response(message=message, status=405, headers=headers)

    @classmethod
    def get_429_response(
        cls, message: str = "", headers: dict | None = None
    ) -> Response:
        message = message or "Too many requests"
        return cls.get_error_response(message=message, status=429, headers=headers)

    @classmethod
    def get_500_response(
        cls, message: str = "", headers: dict | None = None
    ) -> Response:
        message = message or "Internal Error"
        return cls.get_error_response(message=message, status=500, headers=headers)
