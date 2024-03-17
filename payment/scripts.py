# write payment related scripts
import stripe
from django.conf import settings
from payment.models import *
import requests
from constants.commons import handle_exceptions

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_base_url = settings.STRIPE_BASE_URL
def create_stripe_customer(name, email):
	return stripe.Customer.create(name=name, email=email)
	 
def generate_card_token(cardnumber, expmonth, expyear, cvv):
	data= stripe.Token.create(
	        card={
	            "number": str(cardnumber),
	            "exp_month": int(expmonth),
	            "exp_year": int(expyear),
	            "cvc": str(cvv),
	        })
	card_token = data['id']

	return settings.STRIPE_SECRET_KEY

def create_custormer_card_on_stripe(customer_id, source=None):
	return stripe.Customer.create_source(customer_id,source=source)

def fetch_price_list():
	""" this function will return all listed subscription under the product """
	return stripe.Price.list()

def creat_stripe_subscription_payment(customer_id, price_id):
	return stripe.Subscription.create(customer=customer_id,items=[{"price": price_id}])#,payment_behavior="error_if_incomplete", trial_period_days=0)

def fetch_stripe_subscription_list(subscription_id):
	return stripe.Subscription.retrieve(subscription_id)

@handle_exceptions
def fetch_customer_card_list(customer_id):
	url = stripe_base_url+ f"/v1/customers/{customer_id}/cards"
	params = {'limit': 3}
	response = requests.get(url, params=params, auth=(settings.STRIPE_SECRET_KEY, ''))
	if response.status_code == 200:
		return response.json()
	else:
		return response

def cancle_customer_subscription(subscription_id):
	return stripe.Subscription.cancel(subscription_id)