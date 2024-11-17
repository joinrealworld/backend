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
from quiz.models import *
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
from quiz.serializers import *

# Create your views here.
class SendQuizStatusAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		user = request.user
		serializer = QuizStatusSerializer(data=request.data)
		quiz_score, created = QuizScore.objects.get_or_create(user=user)
		if created:
			quiz_score.score = random.randint(70, 92)
			quiz_score.save()
		if serializer.is_valid():
			# Process the valid data
			if serializer.validated_data['status']:
				quiz_score.failer_count = 0
				if created:
					quiz_score.score = random.randint(70, 92)
				else:
					if quiz_score.score is None:
						quiz_score.score = random.randint(70, 92)
					quiz_score.score = quiz_score.score+random.randint(70, 92)/100

				if quiz_score.score < 70:
					quiz_score.score = 70
				elif quiz_score.score > 92:
					quiz_score.score = 92
			else:
				if not created:
					failer_count = quiz_score.failer_count
					quiz_score.failer_count = failer_count + 1
					if quiz_score.failer_count == 5:
						quiz_score.score = quiz_score.score - 1
						quiz_score.failer_count = 0
			quiz_score.score = round(quiz_score.score, 2)
			quiz_score.save()
			return Response(
			    status=status.HTTP_201_CREATED,
			    data={
			        KEY_MESSAGE: "Success",
			        KEY_PAYLOAD: QuizScoreSerializer(quiz_score).data,
			        KEY_STATUS: 0
			})
		return Response(
		    status=status.HTTP_400_BAD_REQUEST,
		    data={
		        KEY_MESSAGE: "Failed",
		        KEY_PAYLOAD: serializer.errors,
		        KEY_STATUS: 0
		    }
		)

	@handle_exceptions
	def get(self, request):
		user = request.user
		quiz_score, created = QuizScore.objects.get_or_create(user=user)
		if quiz_score.score == None:
			return Response(
				    status=status.HTTP_200_OK,
				    data={
				        KEY_MESSAGE: "Success",
				        KEY_PAYLOAD: "Please attent the quiz to get the score.",
				        KEY_STATUS: 0
				})
		else:
			return Response(
			    status=status.HTTP_201_CREATED,
			    data={
			        KEY_MESSAGE: "Success",
			        KEY_PAYLOAD: QuizScoreSerializer(quiz_score).data,
			        KEY_STATUS: 0
			})

