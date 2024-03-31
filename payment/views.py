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
		source = request.data.get("source", None)
		data = {
		    'name': name,
		    'email': email,
		    'source': source
		}
		stripe_customer_data = create_customer(data)
		# Check if the customer already exists
		# existing_customer = CustomerDetails.objects.filter(user=request.user, customer_id__isnull=False).first()
		# if existing_customer:
		#     return Response(
		#         status=status.HTTP_400_BAD_REQUEST,
		#         data={
		#             "message": "Customer already exists",
		#             "payload": existing_customer.data,
		#             "status": 0
		#         }
		#     )

		# # If customer does not exist, create a new one
		# stripe_customer_data = create_stripe_customer(request.user, name, email)

		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": stripe_customer_data,
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
		cus_id = request.data.get("cus_id", None)
		data = {
		    'customer': cus_id,
		    'items[0][price]': price_id,
		    'payment_behavior': 'error_if_incomplete',
		    'off_session': 'true'
		}
		customer_subscription = create_subscription(data)
		# customer_detail = CustomerDetails.objects.filter(user=request.user, customer_id__isnull=False).first()
		# customer_subscription = creat_stripe_subscription_payment(customer_detail.customer_id, price_id)
		# cus_payment = CustomerPayment.objects.create(user = request.user, price_id = price_id, customer_id = customer_detail.customer_id, data = customer_subscription)
		# customer_plan = customer_subscription['items']['data'][0]['plan']
		# cus_payment.status = customer_subscription['status']
		# cus_payment.amount = customer_plan['amount']
		# cus_payment.subscription_id = customer_subscription['id']
		# cus_payment.plan = customer_plan['nickname']
		# cus_payment.status = customer_subscription['status']
		# cus_payment.save()

		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": customer_subscription,
		        "status": 1
		    }
		)

class RetriveSubscriptionAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		user = request.user
		customer_payment = CustomerPayment.objects.filter(user = user).last()
		subscription_data = fetch_stripe_subscription_list(customer_payment.subscription_id)
		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": subscription_data,
		        "status": 1
		    }
		)

class CustomerCardListAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		user = request.user
		customer_detail = CustomerDetails.objects.filter(user=request.user, customer_id__isnull=False).first()
		card_list = fetch_customer_card_list(customer_detail.customer_id)
		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": card_list,
		        "status": 1
		    }
		)


class CancleSubscriptionAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		user = request.user
		subscription_id = request.data.get("subscription_id", None)
		customer_detail = CustomerDetails.objects.filter(user=request.user, customer_id__isnull=False).first()
		customer_payment = CustomerPayment.objects.filter(customer_id = customer_detail.customer_id, subscription_id = subscription_id) #status = "complete"
		cancle_subscription = cancle_customer_subscription(subscription_id)
		if cancle_subscription['status'] in ["canceled", "incomplete_expired"]:
			CancleSubscription.objects.create(user = request.user, status = cancle_subscription['status'], subscription_id = subscription_id, customer_payment = customer_payment.last(), customer_id = customer_detail.customer_id,  data = cancle_subscription)
			customer_payment = customer_payment.last()
			customer_payment.status = cancle_subscription['status']
			customer_payment.save()
		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": cancle_subscription,
		        "status": 1
		    }
		)

class CustomerCardTokenAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		user = request.user
		card_number = request.data.get("card_number", None)
		card_exp_month = request.data.get("card_exp_month", None)
		card_exp_year = request.data.get("card_exp_year", None)
		card_cvc = request.data.get("card_cvc", None)
		card_name = request.data.get("card_name", None)
		data = {
		    'card[number]': card_number,
		    'card[exp_month]': card_exp_month,
		    'card[exp_year]': card_exp_year,
		    'card[cvc]': card_cvc,
		    'card[name]': card_name
		}
		card_token = create_customer_card_token(data)

		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Success",
		        "payload": card_token,
		        "status": 1
		    }
		)


