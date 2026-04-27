import re
from functools import wraps

from django.utils.deprecation import MiddlewareMixin


def no_compress(view_func):
    setattr(view_func, '_no_gzip', True)
    return view_func


class CacheControlMiddleware(MiddlewareMixin):
    HTML_MAX_AGE = 3600
    STATIC_MAX_AGE = 86400
    HASHED_STATIC_MAX_AGE = 31536000

    HASHED_STATIC_PATTERN = re.compile(r"\.[a-f0-9]{8,}\.")

    STATIC_TYPES = ("text/css", "application/javascript", "text/javascript", "application/json", "image/", "font/")

    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(view_func, '_no_gzip', False):
            request._skip_gzip = True

    def __call__(self, request):
        response = self.get_response(request)

        content_type = response.get("Content-Type", "").split(";")[0]

        response["Cross-Origin-Resource-Policy"] = "same-origin"
        response["Cross-Origin-Embedder-Policy"] = "require-corp"
        response["Cross-Origin-Opener-Policy"] = "same-origin"
        response["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' data: ; form-action 'self'; base-uri 'none'; frame-ancestors 'none'; object-src 'none';"

        if content_type == "text/event-stream":
            response["Cache-Control"] = "no-store, no-cache"
            response["X-Do-Not-Compress"] = "1"
        elif content_type.startswith(self.STATIC_TYPES):
            if self.HASHED_STATIC_PATTERN.search(request.path):
                response["Cache-Control"] = f"public, max-age={self.HASHED_STATIC_MAX_AGE}, immutable"
            else:
                response["Cache-Control"] = f"public, max-age={self.STATIC_MAX_AGE}"
        elif content_type == "text/html":
            response["Cache-Control"] = f"public, max-age={self.HTML_MAX_AGE}"

        return response
