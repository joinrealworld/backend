from django.contrib import admin
from payment.models import *

# Register your models here.
class CustomerDetailsAdmin(admin.ModelAdmin):
    fields = ['user', 'uuid','customer_id','data','has_card']
    list_display = ('id', 'user','customer_id','has_card','created_at')
    list_per_page = 25

admin.site.register(CustomerDetails, CustomerDetailsAdmin)

class CustomerPaymentAdmin(admin.ModelAdmin):
    fields = ['user', 'uuid','price_id','customer_id','subscription_id','plan','currency','amount','status','data']
    list_display = ('id','user', 'plan', 'status', 'currency','amount', 'created_at', 'price_id','customer_id','subscription_id',)
    list_per_page = 25

admin.site.register(CustomerPayment, CustomerPaymentAdmin)