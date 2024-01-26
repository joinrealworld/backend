from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.authentication import JWTAuthentication


class InvalidTokenException(APIException):
    status_code = 401
    default_detail = {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [
            {
                "token_class": "AccessToken",
                "token_type": "access",
                "message": "Token is invalid or expired"
            }
        ]
    }

class IsUserAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user

        # Assuming you're using SimpleJWT for token authentication
        access_token = request.auth
        print(access_token)
        refresh_token = JWTAuthentication().get_validated_token(access_token).get('refresh', None)
        print(refresh_token)
        # Check if the access token exists in OutstandingToken for the user
        outstanding_token = OutstandingToken.objects.filter(user=user, token=access_token).first()
        print(OutstandingToken.objects.last().__dict__)
        if outstanding_token:
            return True

        raise InvalidTokenException()

# class IsUserAuthenticated(permissions.IsAuthenticated):
#     def has_permission(self, request, view):
#         user = request.user
#         # jwt_authentication = JWTAuthentication()
#         # access_token = jwt_authentication.get_validated_token(request)
#         outstanding_tokens = OutstandingToken.objects.filter(user=user)
#         print(outstanding_tokens)
#         if outstanding_tokens.exists():
#             return True
#         raise InvalidTokenException()

class IsLoggedInUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_admin

class IsLoggedInUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user