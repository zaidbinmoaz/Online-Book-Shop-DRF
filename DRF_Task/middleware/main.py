from rest_framework import status
from api.models import CustomUser
import jwt
from EpicBooks.settings import SECRET_KEY
from django.http import JsonResponse


class BlockedUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print(get_response)

    def __call__(self, request):
        # print(request.headers['Authorization'], "/////")
        print(request.headers, "/////")

        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return self.get_response(request)

        token = auth_header.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = CustomUser.objects.get(id=payload["user_id"])
        print(user)

        if user.blocked:
            return JsonResponse(
                {"msg": "This user is blocked"},
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            )

        response = self.get_response(request)
        return response


class DeletedUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print(get_response)

    def __call__(self, request):
        print(request.headers, "/////")
        auth_header = request.headers["Authorization"]
        if not auth_header or not auth_header.startswith("Bearer "):
            return self.get_response(request)

        token = auth_header.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = CustomUser.objects.get(id=payload["user_id"])
        print(user)

        if user.deleted:
            return JsonResponse(
                {"msg": "This user is deleted"},
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            )
        response = self.get_response(request)
        return response
