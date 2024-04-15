from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from urllib.parse import parse_qs


@database_sync_to_async
def close_connections():
    close_old_connections()


@database_sync_to_async
def get_user(user_jwt):
    print("*" * 1000)
    try:
        print("here")
        return User.objects.get(id=user_jwt)
    except User.DoesNotExist:
        print("here")
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope, receive, send):
        print("38------")
        # Close old database connections to prevent usage of timed out connections
        close_connections()

        # Get the token
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

        # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            print(e)
            return None
        else:
            #  Then token is valid, decode it
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(decoded_data)
            # Will return a dictionary like -
            # {
            #     "token_type": "access",
            #     "exp": 1568770772,
            #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
            #     "user_id": 6
            # }

            # Get the user using ID
            user = get_user(decoded_data["user_id"])
            print(user)
            print(decoded_data["user_id"])
            print(user)

            # user = get_user_model().objects.get(id=)

        # Return the inner application directly and let it run everything else
        return self.inner(dict(scope, user=decoded_data["user_id"]), receive, send)