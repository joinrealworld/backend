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