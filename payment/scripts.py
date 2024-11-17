# write payment related scripts
import stripe
from django.conf import settings
from payment.models import *
import requests
from constants.commons import handle_exceptions
from user.serializers import UserSimpleSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_base_url = settings.STRIPE_BASE_URL
stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
stripe_product_id = settings.STRIPE_PRODUCT_ID

def create_stripe_customer(user, name, email):
	existing_customer = CustomerDetails.objects.filter(user=user, customer_id__isnull=False).first()
	if existing_customer:
		return existing_customer.data
	stripe_customer_data = stripe.Customer.create(name=name, email=email)
	existing_customer = CustomerDetails.objects.get_or_create(user=user)
	existing_customer.customer_id = stripe_customer_data['id']
	existing_customer.data = stripe_customer_data
	existing_customer.save()
	# existing_customer = CustomerDetails.objects.create(user=user, customer_id=stripe_customer_data['id'], data=stripe_customer_data)
	return existing_customer.data
	 
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
	return stripe.Price.list(product=stripe_product_id)

def creat_stripe_subscription_payment(customer_id, price_id):
	return stripe.Subscription.create(customer=customer_id, items=[{"price": price_id}], payment_behavior="error_if_incomplete",  off_session=True)

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

###
def create_customer_card_token(data):
	url = stripe_base_url+'/v1/tokens'
	headers = {
	    'Authorization': 'Bearer '+stripe_publishable_key,
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'Accept': 'application/json'
	}
	response = requests.post(url, headers=headers, data=data)
	print("67-----", response.json()['id'])

	return response.json()

def create_customer(data, customer_id):
	url = stripe_base_url+'/v1/customers/'+customer_id
	headers = {
	    'Authorization': 'Bearer '+settings.STRIPE_SECRET_KEY,
	    'Content-Type': 'application/x-www-form-urlencoded'
	}
	
	response = requests.post(url, headers=headers, data=data)
	return response.json()

def create_subscription(data):
	url = stripe_base_url+'/v1/subscriptions'
	headers = {
	    'Authorization': 'Bearer '+settings.STRIPE_SECRET_KEY,
	    'Content-Type': 'application/x-www-form-urlencoded'
	}
	response = requests.post(url, headers=headers, data=data)
	return response.json()

def create_user_card_token(user, data):
	url = stripe_base_url+'/v1/tokens'
	headers = {
	    'Authorization': 'Bearer '+stripe_publishable_key,
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'Accept': 'application/json'
	}
	response = requests.post(url, headers=headers, data=data)
	card_token = response.json()['id']
	card_id = response.json()['card']['id']
	customer_details, created = CustomerDetails.objects.get_or_create(user = user, card_id=card_id, has_card=True,)
	customer_details.data=response.json()
	customer_details.save()
	return response.json()

def create_card_customer(user, data):
	url = stripe_base_url+'/v1/customers'
	headers = {
	    'Authorization': 'Bearer '+settings.STRIPE_SECRET_KEY,
	    'Content-Type': 'application/x-www-form-urlencoded'
	}
	
	response = requests.post(url, headers=headers, data=data)
	customer_details = CustomerDetails.objects.filter(user = user)
	for cus_detail in customer_details:
		cus_detail.customer_id = response.json()['id']
		cus_detail.save()
	return response.json()

def create_user_subscription(user, data):
	try:
		url = stripe_base_url+'/v1/subscriptions'
		headers = {
		    'Authorization': 'Bearer '+settings.STRIPE_SECRET_KEY,
		    'Content-Type': 'application/x-www-form-urlencoded'
		}
		response = requests.post(url, headers=headers, data=data)
		CustomerPayment.objects.create(user = user, price_id=data['items[0][price]'], customer_id=data['customer'], subscription_id=response.json()['id'], plan=response.json()['plan']['id'], currency=response.json()['plan']['currency'], amount=response.json()['plan']['amount'], data=response.json(), status=response.json()['status'])
		if response.json()['status'] == 'active':
			user.email_verified = True
			user.save()
			res = user.get_tokens_for_user()
			user_serializer = UserSimpleSerializer(user, many=False)
			return {"token": res['access'], "user": user_serializer.data}
		else:
			return response.json()
	except Exception as e:
		print(e)

def create_stripe_customer_source(user, data):
	response = stripe.Source.create(type="ach_credit_transfer",currency="usd",owner={"email": user.email},)
	return response

def attach_stripe_customer_source(user, customer_id):
	response = stripe.Customer.create_source("cus_9s6XKzkNRiz8i3",source="src_1NfRGv2eZvKYlo2Cv7NAImBL",)
	return response

def fetch_all_stripe_customer():
	return stripe.Customer.list()

def fetch_stripe_customer(customer_id):
	return stripe.Customer.retrieve(customer_id)

def attache_stripe_customer_source(user, customer_id, card_token):
	try:
		res = stripe.Customer.create_source(customer_id,source=card_token)
	except Exception as e:
		print("156----", e)
	customer_details = CustomerDetails.objects.filter(user = user)
	if customer_details:
		customer_details = customer_details.last()
	customer_details.attach_source = res
	customer_details.save()
	return res



