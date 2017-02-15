from django.core import serializers


def deserialize_user(get_response):
    def middleware(request):
        if 'user' in request.session:
            request.user = next(serializers.deserialize("json", request.session["user"])).object
        response = get_response(request)
        return response

    return middleware
