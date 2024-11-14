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
from user.permissions import (
    IsLoggedInUserOrAdmin,
    IsLoggedInUser,
    IsUserAuthenticated
)
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
from django.utils.timezone import now
from django.db.models import Max
from raffel.models import *
from raffel.serializers import *
# Create your views here.


class RaffelCheckoutView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		user = request.user 
		today = now().date()
		existing_raffel = Raffel.objects.filter(user=user, timestamp__date=today).first()

		if existing_raffel:
		    # If a Raffel object exists for today, return the existing object
		    return Response(
		            status=status.HTTP_200_OK,
		            data={
		                KEY_MESSAGE: "You've already checkedout today for the Raffel.",
		                KEY_PAYLOAD:  RaffelSerializer(existing_raffel).data,
		                KEY_STATUS: 1
		            },
		        )

		 # Get the maximum number for today from the Raffel model
		max_number_today = Raffel.objects.filter(timestamp__date=today).aggregate(Max('index'))['index__max'] or 0
		total_index = 1
		if max_number_today == 0:
			index = 1
			pass
		else:
			random_number = random.randint(1, 40)
			total_index = Raffel.objects.filter(timestamp__date=today).first().total_index
			total_index = total_index + random_number
			index = total_index
		# Create a new Raffel object with the next number (incremental index)
		new_raffel = Raffel.objects.create(
		    user=user,
		    index=index,  # Incremental index,
		    total_index = total_index
		)
		user_coin = user.coin
		user_coin = user_coin+50
		user.coin = user_coin
		user.save()
		return Response(
		            status=status.HTTP_201_CREATED,
		            data={
		                KEY_MESSAGE: "Raffel checkout successfully.",
		                KEY_PAYLOAD: RaffelSerializer(new_raffel).data,
		                KEY_STATUS: 1
		            },
		        )

class RaffelPositionAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		user = request.user 
		today = now().date()
		existing_raffel = Raffel.objects.filter(user=user, timestamp__date=today).first()
		today_raffel = Raffel.objects.filter(timestamp__date=today)

		if existing_raffel:
			rafel_status_data = RaffelSerializer(existing_raffel).data
			rafel_status_data["checked"] = True
			# If a Raffel object exists for today, return the existing object
			return Response(
			        status=status.HTTP_200_OK,
			        data={
			            KEY_MESSAGE: "You've already checkedout today for the Raffel.",
			            KEY_PAYLOAD: rafel_status_data,
			            KEY_STATUS: 1
			        },
			    )

		else:
			return Response(
				status=status.HTTP_200_OK,
		            data={
		                KEY_MESSAGE: "You've to checkedout today for the Raffel.",
		                KEY_PAYLOAD:  {"checked":False,"total_index": today_raffel.last().total_index},
		                KEY_STATUS: 1
		            },
				)