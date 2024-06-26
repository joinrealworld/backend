from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.models import AccessTokenLog
from rest_framework import status
from django.utils import timezone

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

class InvalidUserTokenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [
            {
                "token_class": "AccessToken",
                "token_type": "access",
                "message": "User Should Be Admin"
            }
        ]
    }

class IsUserAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            # Authorization header usually looks like "Bearer <token>"
            # Splitting to extract the token part
            _, token = authorization_header.split(' ', 1)

            # Now, you have the token, and you can use it as needed
            # For example, you can print it or perform custom validation
            user = request.user  # Assuming user is authenticated using IsAuthenticated permission
            if AccessTokenLog.objects.filter(user=user, token=token).exists():
                last_award_time = user.last_coins_award_time
                if not last_award_time or timezone.now() - last_award_time >= timezone.timedelta(hours=24):
                    # Give coins to the user
                    user.coin += 50
                    user.save()
                    # Update last award time
                    user.last_coins_award_time = timezone.now()
                user.is_online = True
                user.save()
                return True


        raise InvalidTokenException()


class IsLoggedInUserOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            _, token = authorization_header.split(' ', 1)
            user = request.user
            if AccessTokenLog.objects.filter(user=user, token=token).exists() and user.is_admin:
                return True
        raise InvalidUserTokenException()

class IsLoggedInUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user