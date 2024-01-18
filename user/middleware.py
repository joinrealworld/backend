class DebugAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("AuthenticationMiddleware:", request.user.is_authenticated)
        response = self.get_response(request)
        return response

class TokenInspectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)
        # or
        print(request.get_full_path())
        print(request.build_absolute_uri())
        print("Authorization Header:", request.headers.get('Authorization'))
        print("User:", request.user)
        response = self.get_response(request)
        return response