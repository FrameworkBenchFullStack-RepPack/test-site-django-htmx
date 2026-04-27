from django.middleware.gzip import GZipMiddleware as BaseGZipMiddleware


class GZipMiddleware(BaseGZipMiddleware):
    def process_response(self, request, response):
        if request.path.startswith("/api/live"):
            return response
        return super().process_response(request, response)