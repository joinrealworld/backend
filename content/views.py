from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from rest_framework.generics import (
    ListAPIView,
    GenericAPIView,
    CreateAPIView,
)

# Local Import
from content.models import *
from user.permissions import (
    IsLoggedInUserOrAdmin,
    IsLoggedInUser,
)
from content.serializers import *


class UploadContentView(CreateAPIView):
    """Upload Image View"""
    permission_classes = [IsLoggedInUser]
    serializer_class = UploadContentSerializer
    queryset = Content.objects.all()