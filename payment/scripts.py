# write payment related scripts
import stripe
from django.conf import settings
from payment.models import *

stripe.api_key = settings.STRIPE_SECRET_KEY

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
	return stripe.Subscription.create(customer=customer_id,items=[{"price": price_id}],)