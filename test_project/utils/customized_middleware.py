from rest_framework import status
from rest_framework.response import Response


class VersionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        version = request.META.get('Api-version')
        return self.get_response(request)
        if version in ["v1", "v2"]:
            response = self.get_response(request)
        else:
            response = Response(status=status.HTTP_400_BAD_REQUEST, data="Api-version is required in request header.")
        return response
