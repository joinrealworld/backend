from django.shortcuts import render
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
from datetime import datetime, timedelta, date
from constants.response import KEY_MESSAGE, KEY_PAYLOAD, KEY_STATUS
from constants.commons import handle_exceptions
import random
from django.conf import settings
from payment.models import *
from payment.scripts import *

# Create your views here.
class CreateCustomerAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		name = request.data.get("customer_name", None)
		email = request.data.get("customer_email", None)

		# Check if the customer already exists
		print("41-----", request.user.email)
		existing_customer = CustomerDetails.objects.filter(user=request.user, customer_id__isnull=False).first()
		if existing_customer:
		    return Response(
		        status=status.HTTP_400_BAD_REQUEST,
		        data={
		            "message": "Customer already exists",
		            "payload": existing_customer.data,
		            "status": 0
		        }
		    )

		# If customer does not exist, create a new one
		stripe_customer_data = create_stripe_customer(name, email)
		existing_customer = CustomerDetails.objects.create(user=request.user, customer_id=stripe_customer_data['id'], data=stripe_customer_data)

		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": existing_customer.data,
		        "status": 1
		    }
		)

class CreateCustomerCardAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		card_number = request.data.get("card_number", None)
		exp_month = request.data.get("exp_month", None)
		exp_year = request.data.get("exp_year", None)
		cvv = request.data.get("cvv", None)

		# Check if the customer already exists
		existing_customer = CustomerDetails.objects.filter(user=request.user, customer_id__isnull=False).first()
		if existing_customer:
		    existing_customer.has_card = True
		    existing_customer.save()

		# If customer does not exist, create a new one
		# card_token = generate_card_token(card_number, exp_month, exp_year, cvv)
		card_token = settings.TEST_CARD_TOKEN
		customer_id = CustomerDetails.objects.get(user = request.user).customer_id
		create_card = create_custormer_card_on_stripe(customer_id, settings.TEST_CARD_TOKEN)
		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": create_card,
		        "status": 1
		    }
		)

class FetchSubscriptionsAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": fetch_price_list(),
		        "status": 1
		    }
		)

class CreateSubscriptionAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		price_id = request.data.get("price_id", None)
		customer_detail = CustomerDetails.objects.filter(user=request.user, customer_id__isnull=False).first()
		customer_subscription = creat_stripe_subscription_payment(customer_detail.customer_id, price_id)
		customer_plan = customer_subscription['items']['data'][0]['plan']
		CustomerPayment.objects.create(user = request.user, price_id = price_id, status = customer_subscription['status'],customer_id = customer_detail.customer_id, amount=customer_plan['amount'], subscription_id = customer_subscription['id'], currency=customer_subscription['currency'], plan = customer_plan['nickname'], data = customer_subscription)
		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": customer_subscription,
		        "status": 1
		    }
		)



