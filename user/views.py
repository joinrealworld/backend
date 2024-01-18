# Library Import
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import (
    GenericAPIView,
    UpdateAPIView,
    CreateAPIView,
    ListAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.views import APIView
# Local Import
from user.models import *
from user.permissions import (
    IsLoggedInUserOrAdmin,
    IsLoggedInUser,
)
from user.serializers import *
from rest_framework.pagination import LimitOffsetPagination
from itertools import chain
from rest_framework.settings import api_settings
import random
from django.db.models import Q
from datetime import datetime, timedelta, date
import string
from user.scripts import *

# Create your views here.
class LoginWithPasswordAPIView(GenericAPIView):
    """Custom Login for user to login using password"""

    permission_classes = [AllowAny]
    serializer_class = EmailLoginSerializer

    def post(self, request):
        password = request.data.get('password', None)
        email = request.data.get('email', None)

        if not email:
            return Response({"error": "Please Enter Email or Username or contact number"},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not password:
            return Response({"error": "Please Enter Password"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = None
        if email:
            email = email.lower()
            user = User.objects.filter(email=email).first() or User.objects.filter(username=email).first()

        if user:
            if user.check_password(password):
                token = user.get_tokens_for_user()
                user_serializer = UserSimpleSerializer(user, many=False)
                return Response({"token": token, "user": user_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "User Does Not Exist With This Credentials"},
                                status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({"error": "User Doesn't Exist"}, status.HTTP_422_UNPROCESSABLE_ENTITY)




class SignUpAPIViewAPIView(APIView):
    """End point To Generate/ReGenerate the OTP. Send contact_number and country_code [country_code:str] in parameters"""
    permission_classes = [AllowAny]

    def post(self, request):
        first_name = request.data.get("first_name", None)
        last_name = request.data.get("last_name", None)
        email = request.data.get("email", None)
        
        if not email:
            return Response({"error": "Please Enter Email"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not first_name:
            return Response({"error": "Please Enter First Name"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not last_name:
            return Response({"error": "Please Enter last Name"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = User.objects.filter(email = email)
        if user:
            return Response({"message": "Please make sign in."}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = None
        if email:
            user = User.objects.create(email = email, first_name = first_name, last_name = last_name, referral_code = User.generate_random_string(7))
            otp_to = f"{email}"
            otp_verification = OTPVerification.objects.get_or_create(otp_to=otp_to)[0]
            otp_verification.send_otp()
            return Response({"message": "OTP is sent to your Email", "otp_verification_id": otp_verification.id}, status.HTTP_200_OK)
        else:
            return Response({"error": "Please Enter Email"}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class VerifyOTPAPIView(APIView):
    """End point To Verify the OTP. Send (contact_number and country_code[country_code: srt]) or email and otp in parameters"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email:
            return Response({"error": "Please Enter Email"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = None
        if email != None:
            users = User.objects.filter(email=email) | User.objects.filter(username=email)
            user = users.first()
        else:
            return Response({"error": "Please Enter Email"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if otp == None:
            return Response({"error": "Please Enter OTP"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if user:
            otp_obj = OTPVerification.objects.get(otp_to=email)
            if otp_obj.validate_otp(email, str(otp)):
                if email:
                    if not user.email_verified:
                        user.email_verified = True
                        user.save()

                res = user.get_tokens_for_user()
                user_serializer = UserSimpleSerializer(user, many=False)
                return Response({"token": res['access'], "user": user_serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "OTP is Incorrect or Expired"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({"error": "User Doesn't Exist"}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class SetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("144-----")
        password = request.data.get("password")
        user = request.user
        user.set_password(password)
        user.save()
        return Response({"res": "password stored successfully"}, status=status.HTTP_200_OK)

class FetchProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Request User:", request.user)
        print("Request Auth:", request.auth)
        return Response({"res": UserSimpleSerializer(request.user, many=False).data}, status=status.HTTP_200_OK)



