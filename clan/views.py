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
from clan.models import *
from user.permissions import (
    IsLoggedInUserOrAdmin,
    IsLoggedInUser,
    IsUserAuthenticated
)
# from clan.serializers import *
from rest_framework.pagination import LimitOffsetPagination
from itertools import chain
from rest_framework.settings import api_settings
import random
from django.db.models import Q
from datetime import datetime, timedelta, date
import string
from constants.response import KEY_MESSAGE, KEY_PAYLOAD, KEY_STATUS
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.tokens import OutstandingToken
from notification.scripts import send_account_verification_mail, send_2fa_verification_mail
from constants.commons import handle_exceptions
import random
from user.models import User
from user.serializers import UserSimpleSerializer
from clan.models import *
# Create your views here.
class FetchClanUsersView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		# Step 1: Fetch all dummy users
		users = list(User.objects.filter(is_dummy=True))

		# Step 2: Shuffle the users
		random.shuffle(users)

		# Step 3: Create 10 clans, each with up to 10 users
		lists_of_users = {}
		total_clans = 10
		users_per_clan = 10

		# Only process if there are enough users for the clans
		for i in range(total_clans):
		    clan_name = f'clan{i+1}'
		    start_index = i * users_per_clan
		    end_index = start_index + users_per_clan
		    clan_users = users[start_index:end_index]
		    lists_of_users[clan_name] = clan_users

		# Step 4: Serialize user data using UserSimpleSerializer for each clan
		serialized_clans = {
		    clan: UserSimpleSerializer(user_list, many=True).data for clan, user_list in lists_of_users.items()
		}

		return Response(
		            status=status.HTTP_200_OK,
		            data={
		                KEY_MESSAGE: "Clan Data fetched successfully",
		                KEY_PAYLOAD: serialized_clans,
		                KEY_STATUS: 1
		            },
		        )

class JoinClanUsersView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		user = request.user
		clan_user, created = Clan.objects.get_or_create(user = user)

		if created:
			return Response(
			            status=status.HTTP_200_OK,
			            data={
			                KEY_MESSAGE: "Success",
			                KEY_PAYLOAD: "You're in waiting list to join the clan.",
			                KEY_STATUS: 1
			            },
			        )
		else:
			return Response(
			            status=status.HTTP_200_OK,
			            data={
			                KEY_MESSAGE: "Success",
			                KEY_PAYLOAD: "You've already requested to join the clan, you're in waiting list.",
			                KEY_STATUS: 1
			            },
			        )


