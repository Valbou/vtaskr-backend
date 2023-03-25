from json import dumps
from typing import Optional, Any

from flask import Response


JSON_MIME_TYPE = "application/json"


class ResponseAPI:
    @classmethod
    def get_response(cls, data: Any, status: int, headers: Optional[dict] = None):
        headers = headers or {}
        assert status < 400, f"A status >= 400 is an error not a normal response, given: {status}"
        return Response(
            response=dumps(data),
            status=status,
            headers=headers,
            mimetype=JSON_MIME_TYPE,
            content_type=JSON_MIME_TYPE
        )

    @classmethod
    def get_error_response(cls, message: str, status: int, headers: Optional[dict] = None):
        data = {
            "error": message,
            "status": status
        }
        headers = headers or {}
        return Response(
            response=dumps(data),
            status=status,
            headers=headers,
            mimetype=JSON_MIME_TYPE,
            content_type=JSON_MIME_TYPE
        )
