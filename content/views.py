from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from user.permissions import IsUserAuthenticated
from content.models import *
from user.permissions import (
    IsLoggedInUserOrAdmin,
    IsLoggedInUser,
)
from content.serializers import *



class UploadContentView(APIView):
    """Upload Image View"""
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        serializer = UploadContentSerializer(data=request.data, context={'request': request})

        # Validate the data
        if serializer.is_valid():
            # Save the validated data (create the Content object)
            serializer.save()

            return Response(
                data={
                    "message": "Content uploaded successfully.",
                    "status": 1,
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            # Return validation errors
            return Response(
                data={
                    "message": "Failed to upload content.",
                    "status": 0,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )