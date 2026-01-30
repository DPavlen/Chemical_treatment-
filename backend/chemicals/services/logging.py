import time
from functools import wraps

from chemicals.models import RequestLog
from rest_framework import status
from rest_framework.response import Response


def log_request(
    request,
    method: str,
    smiles: str | None = None,
    has_molfile: bool = False,
    width: int | None = None,
    height: int | None = None,
    image_format: str | None = None,
    success: bool = True,
    error_message: str | None = None,
    response_time_ms: int | None = None,
):
    """Log API request to database."""
    user = request.user if request.user.is_authenticated else None
    RequestLog.objects.create(
        user=user,
        method=method,
        smiles=smiles,
        has_molfile=has_molfile,
        width=width,
        height=height,
        image_format=image_format or "",
        success=success,
        error_message=error_message,
        response_time_ms=response_time_ms,
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
    )


def with_logging(method: str):
    """Decorator that handles timing and logging for API views."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            start_time = time.time()

            try:
                response = view_func(self, request, *args, **kwargs)
                response_time_ms = int((time.time() - start_time) * 1000)

                # Get logging data from request (set by view)
                log_data = getattr(request, "_log_data", {})
                log_request(
                    request=request,
                    method=method,
                    response_time_ms=response_time_ms,
                    success=True,
                    **log_data,
                )
                return response

            except Exception as e:
                response_time_ms = int((time.time() - start_time) * 1000)
                log_data = getattr(request, "_log_data", {})
                log_request(
                    request=request,
                    method=method,
                    response_time_ms=response_time_ms,
                    success=False,
                    error_message=str(e),
                    **log_data,
                )
                return Response(
                    {"error": f"Failed to render molecule: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return wrapper

    return decorator
