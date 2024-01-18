from django.urls import path, include
from rest_framework import routers
from notification import views


# router = routers.DefaultRouter()
# router.register(r'profiles', views.UserViewSet)

# profile_create = views.UserViewSet.as_view({
#     'post': 'create'
# })


urlpatterns = [
	# path('', include(router.urls)),
    # path('login', views.LoginWithPassword.as_view(), name='login'),
	]