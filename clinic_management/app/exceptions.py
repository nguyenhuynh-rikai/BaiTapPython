"""
MediFlow — api/exceptions.py
==============================
Custom exception handler — chuẩn hoá format lỗi toàn API.

Mọi lỗi đều trả về cùng một cấu trúc:
{
    "error": {
        "code":    "VALIDATION_ERROR",
        "message": "Dữ liệu không hợp lệ.",
        "details": { "field": ["message"] }   ← chỉ có khi validation error
    }
}
"""

import logging

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    PermissionDenied as DRFPermissionDenied,
    Throttled,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger("mediflow.api.exceptions")


# ── Mapping exception → (code, http_status) ─────────────────
_EXCEPTION_MAP = {
    NotAuthenticated:    ("NOT_AUTHENTICATED",  status.HTTP_401_UNAUTHORIZED),
    AuthenticationFailed:("AUTHENTICATION_FAILED", status.HTTP_401_UNAUTHORIZED),
    DRFPermissionDenied: ("PERMISSION_DENIED",  status.HTTP_403_FORBIDDEN),
    PermissionDenied:    ("PERMISSION_DENIED",  status.HTTP_403_FORBIDDEN),
    NotFound:            ("NOT_FOUND",          status.HTTP_404_NOT_FOUND),
    Throttled:           ("TOO_MANY_REQUESTS",  status.HTTP_429_TOO_MANY_REQUESTS),
    ValidationError:     ("VALIDATION_ERROR",   status.HTTP_400_BAD_REQUEST),
    ObjectDoesNotExist:  ("NOT_FOUND",          status.HTTP_404_NOT_FOUND),
}


def custom_exception_handler(exc, context) -> Response:
    """
    DRF exception handler tùy chỉnh.
    Gọi handler mặc định trước, rồi transform response.
    """
    # Gọi handler DRF mặc định để xử lý các DRF exceptions
    response = exception_handler(exc, context)

    # Log lỗi server-side
    view = context.get("view")
    view_name = view.__class__.__name__ if view else "unknown"

    code, http_status = _EXCEPTION_MAP.get(
        type(exc),
        ("SERVER_ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR),
    )

    if http_status >= 500:
        logger.exception(
            "Unhandled exception in %s: %s", view_name, exc,
            extra={"view": view_name},
        )
    else:
        logger.warning(
            "API error [%s] in %s: %s", code, view_name, exc,
        )

    # Build error body
    error_body: dict = {"code": code, "message": str(exc.detail if hasattr(exc, "detail") else exc)}

    # Thêm field-level details cho ValidationError
    if isinstance(exc, ValidationError) and isinstance(exc.detail, dict):
        error_body["details"] = _flatten_errors(exc.detail)
    elif isinstance(exc, ValidationError) and isinstance(exc.detail, list):
        error_body["message"] = exc.detail[0] if exc.detail else "Dữ liệu không hợp lệ."

    # Nếu DRF đã trả response thì chỉ transform body
    if response is not None:
        response.data = {"error": error_body}
        return response

    # Lỗi không phải DRF (Django exception, unexpected…)
    return Response(
        {"error": error_body},
        status=http_status,
    )


def _flatten_errors(detail: dict, prefix: str = "") -> dict:
    """Flatten nested validation errors thành dict phẳng."""
    result = {}
    for key, value in detail.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(_flatten_errors(value, full_key))
        elif isinstance(value, list):
            result[full_key] = [str(v) for v in value]
        else:
            result[full_key] = str(value)
    return result
