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
    IsUserAuthenticated
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
from constants.response import KEY_MESSAGE, KEY_PAYLOAD
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.tokens import OutstandingToken
from notification.scripts import send_account_verification_mail

# Create your views here.
class LoginWithPasswordAPIView(GenericAPIView):
    """Custom Login for user to login using password"""

    permission_classes = [AllowAny]
    serializer_class = EmailLoginSerializer

    def post(self, request):
        password = request.data.get('password', None)
        email = request.data.get('email', None)

        if not email:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "error",
                    KEY_PAYLOAD: "Please Enter Email or Username or contact number"
                },
            )

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
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={
                        KEY_MESSAGE: "user login successful.",
                        KEY_PAYLOAD: {"token": token, "user": user_serializer.data}
                    },
                )
            else:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "User Does Not Exist With This Credentials"
                    },
                )
        else:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "User Doesn't Exist"
                    },
                )




class SignUpAPIViewAPIView(APIView):
    """End point To Generate/ReGenerate the OTP. Send contact_number and country_code [country_code:str] in parameters"""
    permission_classes = [AllowAny]

    def post(self, request):
        first_name = request.data.get("first_name", None)
        last_name = request.data.get("last_name", None)
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        
        if not email:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Enter Email"
                    },
                )
        if not password:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Enter Password."
                    },
                )

        if not first_name:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Enter First Name"
                    },
                )

        if not last_name:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Enter last Name"
                    },
                )

        user = User.objects.filter(email = email)
        if user:
            if user.last().email_verified == False:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Verify Your Email."
                    },
                )

            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please make sign in."
                    },
                )

        user = None
        if email:
            user = User.objects.create(email = email, first_name = first_name, last_name = last_name, referral_code = User.generate_random_string(7))
            user.set_password(password)
            user.email_verified = False
            user.save()
            verification_token = generate_verification_token()
            verification_link = generate_user_account_verification_link(verification_token, "verify_email")
            EmailVerification.objects.get_or_create(email_to = user, verification_token = verification_token)
            send_account_verification_mail(first_name, verification_link, email)

            return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Sucess",
                        KEY_PAYLOAD: "Please Verify Your Email Address through sent email"
                    },
                )
        else:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Enter Email"
                    },
                )

class VerifyEmailAPIView(APIView):
    """End point To Verify the OTP. Send (contact_number and country_code[country_code: srt]) or email and otp in parameters"""
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get("token")

        if not token:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Provide Token"
                    },
                )

        user = None
        if token != None:
            email_verification = EmailVerification.objects.filter(verification_token=token)
        else:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Provide Token"
                    },
                )

        if not email_verification:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Verify Email through Signup or Forgot Password."
                    },
                )
        user = email_verification.last().email_to
        if user:
            email_verification = email_verification.last()
            if email_verification.validate_email(user, token):
                if token:
                    if not user.email_verified:
                        user.email_verified = True
                        user.save()

                res = user.get_tokens_for_user()
                user_serializer = UserSimpleSerializer(user, many=False)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Email verfied successfully.",
                        KEY_PAYLOAD: {"token": res['access'], "user": user_serializer.data}
                    },
                )
            else:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Link is Incorrect or Expired"
                    },
                )
        else:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "User Doesn't Exist"
                    },
                )


class SetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        password = request.data.get("password", None)
        user = request.user
        if password is None:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please provide the New Password."
                    },
                )

        if not request.user.is_authenticated:
            token = request.data.get("token", None)
            if token is None:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Token is not Provided."
                    },
                )
            email_verification = EmailVerification.objects.filter(verification_token=token)
            if not email_verification:
                return Response(
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        data={
                            KEY_MESSAGE: "error",
                            KEY_PAYLOAD: "Please Verify Email through Signup or Forgot Password."
                        },
                    )
            user = email_verification.last().email_to
            if user:
                email_verification = email_verification.last()
                if email_verification.validate_email(user, token):
                    if token:
                        if not user.email_verified:
                            user.email_verified = True
                        user.set_password(password)
                        user.save()

                        res = user.get_tokens_for_user()
                        user_serializer = UserSimpleSerializer(user, many=False)
                        return Response(
                            status=status.HTTP_200_OK,
                            data={
                                KEY_MESSAGE: "Email verfied successfully.",
                                KEY_PAYLOAD: {"token": res['access'], "user": user_serializer.data}
                            },
                        )
                else:
                    return Response(
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        data={
                            KEY_MESSAGE: "error",
                            KEY_PAYLOAD: "Link is Incorrect or Expired"
                        },
                    )

        user.set_password(password)
        user.save()
        return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Success",
                        KEY_PAYLOAD: "Password stored successfully"
                    },
                )

class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get("email", None)
        if email is None:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Provide Email"
                    },
                )
        user = User.objects.filter(email = email)
        if not user:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please make sign up."
                    },
                )
        user = user.last()
        if user.email_verified == False:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please verify email."
                    },
                )
        verification_token = generate_verification_token()
        verification_link = generate_user_account_verification_link(verification_token, "reset_password")
        EmailVerification.objects.get_or_create(email_to = user, verification_token = verification_token)
        send_account_verification_mail(user.first_name, verification_link, email)

        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "Sucess",
                    KEY_PAYLOAD: "Password Reset Link sent to your mail box"
                },
            )

class FetchProfileAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def get(self, request):
        return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Profile fetched successfully",
                        KEY_PAYLOAD: UserSimpleSerializer(request.user, many=False).data
                    },
                )

class ChangeUserNameAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def patch(self, request):
        username = request.data.get("username", None)
        user = request.user
        if username is None:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "Error",
                        KEY_PAYLOAD: "Username can not be empty."
                    },
                )
        user.username = username
        user.save()
        return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Success",
                        KEY_PAYLOAD: "Username updated successfully."
                    },
                )

class ChangePasswordAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": serializer.errors,
                }
            )

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        user = request.user

        if user.check_password(old_password):
            if old_password == new_password:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        "message": "Error",
                        "payload": "New password can not be similar to the old password."
                    },
                )
            user.set_password(new_password)
            user.save()
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message": "Success",
                    "payload": "Password updated successfully."
                },
            )
        else:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    "message": "Error",
                    "payload": "Old Password doesn't match with the database."
                },
            )

class ChangeStatusAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def patch(self, request):
        serializer = ChangeStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": serializer.errors,
                }
            )

        user_status = serializer.validated_data["status"]
        user = request.user
        user.status = user_status
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Status updated successfully."
            }
        )

    def delete(self, request):
        user = request.user

        # Validate if the user has an existing status to delete
        if not user.status:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": "User does not have an existing status to delete.",
                }
            )

        # Update user status
        user.status = ""
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Status updated successfully.",
            }
        )


class ChangeInvisibleAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def patch(self, request):
        serializer = ChangeInvisibleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": serializer.errors,
                }
            )
        invisible = serializer.validated_data["invisible"]
        user = request.user
        user.invisible = invisible
        user.save()
        return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Success",
                        KEY_PAYLOAD: "Inivisible updated successfully."
                    },
                )

    
class ChangeAvatarAPIView(APIView):
    permission_classes = [IsUserAuthenticated]
    parser_classes = [MultiPartParser]

    def patch(self, request):
        serializer = AvatarSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": serializer.errors,
                }
            )

        # Update user avatar
        user = request.user
        user.avatar = serializer.validated_data['avatar']
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": UploadAvatarSerializer(user).data,
            }
        )

    def delete(self, request):
        user = request.user

        # Validate if the user has an existing avatar to delete
        if not user.avatar:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": "User does not have an existing avatar to remove.",
                }
            )

        # Update user avatar
        user.avatar = ""
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Avatar removed successfully.",
            }
        )

class ChangeBackgroundAPIView(APIView):
    permission_classes = [IsUserAuthenticated]
    parser_classes = [MultiPartParser]

    def patch(self, request):
        serializer = BackgroundSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": serializer.errors,
                }
            )

        # Update user avatar
        user = request.user
        user.background = serializer.validated_data['background']
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": UploadBackgroundSerializer(user).data,
            }
        )

    def delete(self, request):
        user = request.user

        # Validate if the user has an existing avatar to delete
        if not user.background:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": "User does not have an existing background to remove.",
                }
            )

        # Update user avatar
        user.background = ""
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Background removed successfully.",
            }
        )

class ChangeBioAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def patch(self, request):
        serializer = ChangeBioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": serializer.errors,
                }
            )

        bio = serializer.validated_data.get('bio', '').strip()

        # Update user bio
        user = request.user
        user.bio = bio
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Bio Updated Successfully.",
            }
        )

    def delete(self, request):
        user = request.user

        # Validate if the user has an existing avatar to delete
        if not user.bio:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": "User does not have an existing bio to remove.",
                }
            )

        # Update user avatar
        user.bio = ""
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Bio removed successfully.",
            }
        )
class SingleDeviceLogoutAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def get(self, request):
        authorization_header = request.headers.get('Authorization')
        _, token = authorization_header.split(' ', 1)
        AccessTokenLog.objects.filter(user=request.user, token=token).delete()
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Logout from All device successful",
            }
        )

class AllDeviceLogoutAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def get(self, request):
        AccessTokenLog.objects.filter(user=request.user).delete()
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Logout from All device successful",
            }
        )

class UserFeedbackAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        # Use the serializer for input validation
        serializer = FeedbackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": serializer.errors,
                }
            )

        # If validation passes, create a Feedback instance
        FeedBack.objects.create(user=request.user, message=serializer.validated_data['message'])
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Feedback sent successfully.",
            }
        )



class UpdateThemeAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def patch(self, request):
        serializer = UpdateThemeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": serializer.errors,
                }
            )

        # If validation passes, update the user's theme
        user = request.user
        user.theme = serializer.validated_data['theme']
        user.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Theme updated successfully.",
            }
        )

class UpdateSoundEffectAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def patch(self, request):
        serializer = UpdateSoundEffectSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "Validation Error",
                    "payload": serializer.errors,
                }
            )

        # If validation passes, update the user's sound_effect
        user = request.user
        user.sound_effect = serializer.validated_data['sound_effect']
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Success",
                "payload": "Sound Effect updated successfully.",
            }
        )

