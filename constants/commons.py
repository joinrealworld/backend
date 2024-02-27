from constants.response import KEY_MESSAGE, KEY_PAYLOAD, KEY_STATUS
from rest_framework import status
from rest_framework.response import Response
from functools import wraps

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
        	return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
					KEY_MESSAGE: "Exception Occured",
					KEY_PAYLOAD: f"An error occurred: {str(e)}",
					KEY_STATUS: -1
                },
            )
    return wrapper