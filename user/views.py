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
from constants.response import KEY_MESSAGE, KEY_PAYLOAD, KEY_STATUS
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.tokens import OutstandingToken
from notification.scripts import send_account_verification_mail, send_2fa_verification_mail
from constants.commons import handle_exceptions
import random
from payment.scripts import *

# Create your views here.
class LoginWithPasswordAPIView(GenericAPIView):
    """Custom Login for user to login using password"""

    permission_classes = [AllowAny]
    serializer_class = EmailLoginSerializer

    @handle_exceptions
    def post(self, request):
        password = request.data.get('password', None)
        email = request.data.get('email', None)
        code = request.data.get('fa_code', None)
        if not email:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "error",
                    KEY_PAYLOAD: "Please enter your email!",
                    KEY_STATUS: 0
                },
            )

        if not password:
            return Response({"error": "Please enter your password!"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = None
        if email:
            email = email.lower()
            user = User.objects.filter(email=email).first() or User.objects.filter(username=email).first()
        if user:
            if user.email_verified == False:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please verify your email address!",
                        KEY_STATUS: -1
                    },
                )
            if user.check_password(password):
                if user.fa:
                    if code is None:
                        if user.fa_type == "email":
                            new_code = ''.join(random.choices('0123456789', k=4))
                            FAVerification.objects.create(fa_code = new_code, email_to = user)
                            send_2fa_verification_mail("Join Real World | 2FA Authentication",user.first_name, new_code, email)
                        return Response(
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            data={
                                KEY_MESSAGE: "error",
                                KEY_PAYLOAD: "Please Enter 2FA verification Code.",
                                KEY_STATUS: 0
                            },
                        )
                    if not user.verify_2fa_authentication(code):
                        return Response(
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            data={
                                KEY_MESSAGE: "error",
                                KEY_PAYLOAD: "Incorrect code! 2FA verification failed.",
                                KEY_STATUS: -1
                            },
                        )
                token = user.get_tokens_for_user()
                user_serializer = UserSimpleSerializer(user, many=False)
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={
                        KEY_MESSAGE: "user login successful.",
                        KEY_PAYLOAD: {"token": token, "user": user_serializer.data},
                        KEY_STATUS: 1
                    },
                )
            else:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "The password is incorrect!",
                        KEY_STATUS: -1
                    },
                )
        else:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Email doesn't exist!",
                        KEY_STATUS: 0
                    },
                )




class SignUpAPIViewAPIView(APIView):
    """End point To Generate/ReGenerate the OTP. Send contact_number and country_code [country_code:str] in parameters"""
    permission_classes = [AllowAny]

    @handle_exceptions
    def post(self, request):
        first_name = request.data.get("first_name", None)
        last_name = request.data.get("last_name", None)
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        card_number = request.data.get("card_number", None)
        card_exp_month = request.data.get("card_exp_month", None)
        card_exp_year = request.data.get("card_exp_year", None)
        card_cvc = request.data.get("card_cvc", None)
        card_name = request.data.get("card_name", None)
        price_id = request.data.get("price_id", None)

        if card_number is None or card_exp_month is None or card_exp_year is None or card_cvc is None or card_name is None:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Enter Card Details",
                        KEY_STATUS: 0
                    },
                )
        
        if not email:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please enter your email!",
                        KEY_STATUS: 0
                    },
                )
        if not password:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please enter your password!",
                        KEY_STATUS: 0
                    },
                )

        if not first_name:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please enter your first name!",
                        KEY_STATUS: 0
                    },
                )

        if not last_name:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please enter your last name!",
                        KEY_STATUS: 0
                    },
                )

        user = User.objects.filter(email = email)
        if user:
            if user.last().email_verified == False:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "User already exists. Please verify your email address to login.",
                        KEY_STATUS: -1
                    },
                )

            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "User already exists. Please login.",
                        KEY_STATUS: -1
                    },
                )

        user = None
        if email:
            user = User.objects.create(email = email, first_name = first_name, last_name = last_name, referral_code = User.generate_random_string(7))
            user.set_password(password)
            user.email_verified = False
            user.save()
            card_data = {
                'card[number]': card_number,
                'card[exp_month]': card_exp_month,
                'card[exp_year]': card_exp_year,
                'card[cvc]': card_cvc,
                'card[name]': card_name
            }
            card_token = create_user_card_token(user, card_data)
            card_token = card_token['id']
            cus_data = {
                'name': first_name + " " + last_name,
                'email': email,
                'source': card_token
            }
            customer_data = create_card_customer(user, cus_data)
            customer_id = customer_data['id']
            card_token = create_user_card_token(user, card_data)
            card_token = card_token['id']
            create_customer_source = attache_stripe_customer_source(user, customer_id, card_token)
            subscription_data = {
                'customer': customer_id,
                'items[0][price]': price_id,
                'payment_behavior': 'error_if_incomplete',
                'off_session': 'true'
            }

            subscription_data = create_user_subscription(user, subscription_data)
            # verification_token = generate_verification_token()
            # verification_link = generate_user_account_verification_link(verification_token, "verify-email?e=")
            # EmailVerification.objects.get_or_create(email_to = user, verification_token = verification_token)
            # send_account_verification_mail("Verify your email to create your Join Real World Account",first_name, verification_link, email)
            data = {
                'data': subscription_data,
                "customer_id": customer_id,
                "price_id": price_id
            }
            return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Sucess",
                        KEY_PAYLOAD: data,
                        KEY_STATUS: 1
                    },
                )
        else:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please enter your email!",
                        KEY_STATUS: 0
                    },
                )

class VerifyEmailAPIView(APIView):
    """End point To Verify the OTP. Send (contact_number and country_code[country_code: srt]) or email and otp in parameters"""
    permission_classes = [AllowAny]

    @handle_exceptions
    def get(self, request):
        token = request.query_params.get("t")

        if not token:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please provide a token!",
                        KEY_STATUS: 0
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
                        KEY_PAYLOAD: "Please provide a token!",
                        KEY_STATUS: 0
                    },
                )

        if not email_verification:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please Verify Email through Signup or Forgot Password.",
                        KEY_STATUS: 0
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
                        KEY_PAYLOAD: {"token": res['access'], "user": user_serializer.data},
                        KEY_STATUS: 1
                    },
                )
            else:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "The verification link has expired.", 
                        KEY_STATUS: 0
                    },
                )
        else:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "User doesn't exist!",
                        KEY_STATUS: -1
                    },
                )


class SetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    @handle_exceptions
    def post(self, request):
        password = request.data.get("password", None)
        user = request.user
        if password is None:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please provide a new password.",
                        KEY_STATUS: 0
                    },
                )

        if not request.user.is_authenticated:
            token = request.data.get("token", None)
            if token is None:
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "The token not provided",
                        KEY_STATUS: 0
                    },
                )
            email_verification = EmailVerification.objects.filter(verification_token=token)
            if not email_verification:
                return Response(
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        data={
                            KEY_MESSAGE: "error",
                            KEY_PAYLOAD: "Please Verify Email through Signup or Forgot Password.",
                            KEY_STATUS: 0
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
                                KEY_MESSAGE: "Email verified successfully.",
                                KEY_PAYLOAD: {"token": res['access'], "user": user_serializer.data},
                                KEY_STATUS: 0
                            },
                        )
                else:
                    return Response(
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        data={
                            KEY_MESSAGE: "error",
                            KEY_PAYLOAD: "The reset password link has expired.",
                            KEY_STATUS: 0
                        },
                    )

        user.set_password(password)
        user.save()
        return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Success",
                        KEY_PAYLOAD: "Password stored successfully",
                        KEY_STATUS: 1
                    },
                )

class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    @handle_exceptions
    def get(self, request):
        email = request.query_params.get("email", None)
        if email is None:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please enter your email!",
                        KEY_STATUS: 0
                    },
                   
                )
        user = User.objects.filter(email = email)
        if not user:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "The provided email doesn't exist! Please check your email or register.",
                        KEY_STATUS: 0
                    },
                )
        user = user.last()
        if user.email_verified == False:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "error",
                        KEY_PAYLOAD: "Please verify your email address!",
                        KEY_STATUS: 0
                    },
                )
        verification_token = generate_verification_token()
        verification_link = generate_user_account_verification_link(verification_token, "reset-password?t=")
        EmailVerification.objects.get_or_create(email_to = user, verification_token = verification_token)
        send_account_verification_mail("Reset Your Password for Join Real World", user.first_name, verification_link, email)

        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "Success",
                    KEY_PAYLOAD: "Password Reset Link sent to your mail box",
                    KEY_STATUS: 1
                },
            )

class FetchProfileAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request):
        return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Profile fetched successfully",
                        KEY_PAYLOAD: UserSimpleSerializer(request.user, many=False).data,
                        KEY_STATUS: 1
                    },
                )

class ChangeUserNameAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        username = request.data.get("username", None)
        user = request.user
        if username is None:
            return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data={
                        KEY_MESSAGE: "Error",
                        KEY_PAYLOAD: "Please provide a username!",
                        KEY_STATUS: 0
                    },
                )
        user.username = username
        user.save()
        return Response(
                    status=status.HTTP_200_OK,
                    data={
                        KEY_MESSAGE: "Success",
                        KEY_PAYLOAD: "Username updated successfully.",
                        KEY_STATUS: 1
                    },
                )

class ChangePasswordAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
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
                        KEY_MESSAGE: "Error",
                        KEY_PAYLOAD: "New password is similar to the old password!",
                        KEY_STATUS: 0
                    },
                )
            user.set_password(new_password)
            user.save()
            return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "Success",
                    KEY_PAYLOAD: "Password updated successfully.",
                    KEY_STATUS: 1
                },
            )
        else:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "Old password is incorrect!",
                    KEY_STATUS: 0
                },
            )

class ChangeStatusAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        serializer = ChangeStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
                }
            )

        user_status = serializer.validated_data["status"]
        user = request.user
        user.status = user_status
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Status updated successfully.",
                KEY_STATUS: 1
            }
        )

    @handle_exceptions
    def delete(self, request):
        user = request.user

        # Validate if the user has an existing status to delete
        if not user.status:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: "User does not have an existing status to delete.",
                    KEY_STATUS: 0
                }
            )

        # Update user status
        user.status = ""
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Status updated successfully.",
                KEY_STATUS: 1
            }
        )


class ChangeInvisibleAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        serializer = ChangeInvisibleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
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
                        KEY_PAYLOAD: "Invisible updated successfully.",
                        KEY_STATUS: 1
                    },
                )

    
class ChangeAvatarAPIView(APIView):
    permission_classes = [IsUserAuthenticated]
    parser_classes = [MultiPartParser]

    @handle_exceptions
    def patch(self, request):
        serializer = AvatarSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
                }
            )

        # Update user avatar
        user = request.user
        user.avatar = serializer.validated_data['avatar']
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: UploadAvatarSerializer(user).data,
                KEY_STATUS: 1
            }
        )

    @handle_exceptions
    def delete(self, request):
        user = request.user

        # Validate if the user has an existing avatar to delete
        if not user.avatar:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: "User does not have an existing avatar to remove.",
                    KEY_STATUS: 0
                }
            )

        # Update user avatar
        user.avatar = ""
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Avatar removed successfully.",
                KEY_STATUS: 1
            }
        )

class ChangeBackgroundAPIView(APIView):
    permission_classes = [IsUserAuthenticated]
    parser_classes = [MultiPartParser]

    @handle_exceptions
    def patch(self, request):
        serializer = BackgroundSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
                }
            )

        # Update user avatar
        user = request.user
        user.background = serializer.validated_data['background']
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: UploadBackgroundSerializer(user).data,
                KEY_STATUS: 1
            }
        )

    @handle_exceptions
    def delete(self, request):
        user = request.user

        # Validate if the user has an existing avatar to delete
        if not user.background:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: "User does not have an existing background to remove.",
                    KEY_STATUS: 1
                }
            )

        # Update user avatar
        user.background = ""
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Background removed successfully.",
                KEY_STATUS: 1
            }
        )

class ChangeBioAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        serializer = ChangeBioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
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
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Bio Updated Successfully.",
                KEY_STATUS: 1
            }
        )

    @handle_exceptions
    def delete(self, request):
        user = request.user

        # Validate if the user has an existing avatar to delete
        if not user.bio:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: "User does not have an existing bio to remove.",
                    KEY_STATUS: 0
                }
            )

        # Update user avatar
        user.bio = ""
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Bio removed successfully.",
                KEY_STATUS: 1
            }
        )
class SingleDeviceLogoutAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request):
        authorization_header = request.headers.get('Authorization')
        _, token = authorization_header.split(' ', 1)
        AccessTokenLog.objects.filter(user=request.user, token=token).delete()
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Logout from All device successful",
                KEY_STATUS: 1
            }
        )

class AllDeviceLogoutAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request):
        AccessTokenLog.objects.filter(user=request.user).delete()
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Logout from All device successful",
                KEY_STATUS: 1
            }
        )

class UserFeedbackAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def post(self, request):
        # Use the serializer for input validation
        serializer = FeedbackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
                }
            )

        # If validation passes, create a Feedback instance
        FeedBack.objects.create(user=request.user, message=serializer.validated_data['message'])
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Feedback sent successfully.",
                KEY_STATUS: 1
            }
        )



class UpdateThemeAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        serializer = UpdateThemeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
                }
            )

        # If validation passes, update the user's theme
        user = request.user
        user.theme = serializer.validated_data['theme']
        user.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Theme updated successfully.",
                KEY_STATUS: 1
            }
        )

class UpdateSoundEffectAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        serializer = UpdateSoundEffectSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
                }
            )

        # If validation passes, update the user's sound_effect
        user = request.user
        user.sound_effect = serializer.validated_data['sound_effect']
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Sound Effect updated successfully.",
                KEY_STATUS: 1
            }
        )

class ChangeAuthenticationAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        serializer = UpdateAuthenticationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    KEY_MESSAGE: "Validation Error",
                    KEY_PAYLOAD: serializer.errors,
                    KEY_STATUS: 0
                }
            )

        # If validation passes, update the user's sound_effect
        user = request.user
        user.fa = serializer.validated_data['authentication']
        user.fa_type = serializer.validated_data['authentication_type']
        if user.fa and user.fa_type == "code":
            user.fa_code = serializer.validated_data['authentication_code']
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Authentication updated successfully.",
                KEY_STATUS: 1
            }
        )

class SendVerificationMailAPIView(APIView):
    permission_classes = [AllowAny]

    @handle_exceptions
    def get(self, request):
        email = request.query_params.get("email")
        try:
            user = User.objects.get(email = email)
        except Exception as e:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "Email doesn't exist! Please register first.",
                    KEY_STATUS: 1
                }
            )
        verification_token = generate_verification_token()
        verification_link = generate_user_account_verification_link(verification_token, "verify-email?e=")
        EmailVerification.objects.get_or_create(email_to = user, verification_token = verification_token)
        send_account_verification_mail("Verify your email to create your Join Real World Account",user.first_name, verification_link, email)
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Verification email sent successfully.",
                KEY_STATUS: 1
            }
        )


class CheckEmailAPIView(APIView):
    permission_classes = [AllowAny]

    @handle_exceptions
    def post(self, request):
        email = request.data.get("email", None)
        try:
            user = User.objects.get(email = email)
        except Exception as e:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    KEY_MESSAGE: "Success",
                    KEY_PAYLOAD: "Email doesn't exist!.",
                    KEY_STATUS: 1
                }
            )
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Error",
                KEY_PAYLOAD: "Email already exists! Please try with another email address.",
                KEY_STATUS: 0
            }
        )

class PurchesEmojiAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def post(self, request):
        serializer = PurchesEmojiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        emoji = serializer.validated_data.get('emoji')
        price = serializer.validated_data.get('price')
        user_coin = request.user.coin

        if user_coin < price:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "You don't have enough coins.",
                    KEY_STATUS: 0
                }
            )

        user_emoji = UserPurchesedEmoji.objects.create(emoji=emoji, price=price, user=request.user)
        request.user.coin -= price
        request.user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: f"{emoji} purchased successfully.",
                KEY_STATUS: 1
            }
        )

class PurchaseIdentityBoosterAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def post(self, request):
        user_coin = request.user.coin

        if user_coin < 20:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "You should have atleast 20 coins.",
                    KEY_STATUS: 0
                }
            )

        request.user.coin -= 20
        request.user.identity_booster = True
        request.user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: f"identity Booster purchased successfully.",
                KEY_STATUS: 1
            }
        )

class PurchesTuneAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def post(self, request):
        serializer = PurchesTuneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tune = serializer.validated_data.get('tune')
        price = serializer.validated_data.get('price')
        user_coin = request.user.coin

        if user_coin < price:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "You don't have enough coins.",
                    KEY_STATUS: 0
                }
            )

        user_tune = UserPurchesedTune.objects.create(tune=tune, price=price, user=request.user)
        request.user.coin -= price
        request.user.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: f"{tune} purchased successfully.",
                KEY_STATUS: 1
            }
        )

class ListMyEmojiAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request):
        user_emojies = UserPurchesedEmoji.objects.filter(user=request.user)
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: UserPurchesedEmojiSerializer(user_emojies, many=True).data,
                KEY_STATUS: 1
            }
        )

class ListMyTuneAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request):
        user_tune = UserPurchesedTune.objects.filter(user=request.user)
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: UserPurchesedTuneSerializer(user_tune, many=True).data,
                KEY_STATUS: 1
            }
        )


class FetchWallPapaerAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request):
        wallpapers = WallPaper.objects.all()
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: WallPaperSerializer(wallpapers, many=True, context={'user': request.user}).data,
                KEY_STATUS: 1
            }
        )

class BuyWallPapaerAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def post(self, request):
        wallpaper_uuid = request.data.get('uuid', None)
        wallpaper = WallPaper.objects.get(uuid = wallpaper_uuid)
        if UserWallPaper.objects.filter(user=request.user, wallpaper=wallpaper).exists():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "You have already bought this wallpaper.",
                    KEY_STATUS: 0
                }
            )
        if wallpaper.price > request.user.coin:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "You don't have enough coins.",
                    KEY_STATUS: 0
                }
            )
        UserWallPaper.objects.get_or_create(is_purchase=True, user=request.user, wallpaper=wallpaper)
        request.user.coin -= wallpaper.price
        request.user.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Wallpaper Purchsed Successfully.",
                KEY_STATUS: 1
            }
        )

class ChangeWallPapaerAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        wallpaper_uuid = request.data.get('uuid', None)
        wallpaper = WallPaper.objects.get(uuid = wallpaper_uuid)
        if UserWallPaper.objects.filter(user=request.user, wallpaper=wallpaper).exists():
            user_wallpapers = UserWallPaper.objects.filter(user=request.user, is_purchase=True, selected = True)
            for wallpaper in user_wallpapers:
                wallpaper.selected = False
                wallpaper.save()
            selected_wallpaper = UserWallPaper.objects.get(user=request.user, wallpaper=wallpaper)
            selected_wallpaper.selected = True
            selected_wallpaper.save()
        else:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "You need to purchase wallpaper.",
                    KEY_STATUS: 0
                }
            )

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Wallpaper Changed Successfully.",
                KEY_STATUS: 1
            }
        )

class ChangeTuneAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        tune_uuid = request.data.get('uuid', None)
        if UserPurchesedTune.objects.filter(uuid = tune_uuid).exists():
            user_tune = UserPurchesedTune.objects.get(uuid = tune_uuid)
            selected_tune = UserPurchesedTune.objects.get(uuid = tune_uuid)
            selected_tune.selected = True
            selected_tune.save()
        else:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "You need to purchase tune.",
                    KEY_STATUS: 0
                }
            )

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Tune Changed Successfully.",
                KEY_STATUS: 1
            }
        )

class ChangeEmojiAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        # emoji_uuid = request.data.get('uuid', None)
        emoji = request.data.get('emoji', None)
        user = request.user
        # if UserPurchesedEmoji.objects.filter(uuid = emoji_uuid).exists():
        if user.identity_booster:
            # user_emoji = UserPurchesedEmoji.objects.get(uuid = emoji_uuid)
            # selected_emoji = UserPurchesedEmoji.objects.get(uuid = emoji_uuid)
            # selected_emoji.selected = True
            # selected_emoji.save()
            # request.user.username = str(request.user.username) + str(selected_emoji.emoji)
            request.user.selected_emoji = str(emoji)
            request.user.save()
        else:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    KEY_MESSAGE: "Error",
                    KEY_PAYLOAD: "You need to purchase Emoji.",
                    KEY_STATUS: 0
                }
            )

        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Emoji Changed Successfully.",
                KEY_STATUS: 1
            }
        )

class SetOfflineAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def patch(self, request):
        user = request.user
        user.is_online = False 
        user.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: "Set User Offline Successfully.",
                KEY_STATUS: 1
            }
        )
