from django.urls import path, include
from rest_framework import routers
from user import views


# router = routers.DefaultRouter()
# router.register(r'profiles', views.UserViewSet)

# profile_create = views.UserViewSet.as_view({
#     'post': 'create'
# })


urlpatterns = [
	# path('', include(router.urls)),
    path('login', views.LoginWithPasswordAPIView.as_view(), name='login-with-password'),
    path('signup', views.SignUpAPIViewAPIView.as_view(), name='sign-up'),
    path('verify_otp', views.VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('set_password', views.SetPasswordAPIView.as_view(), name='set-password'),
    path('profile', views.FetchProfileAPIView.as_view(), name='get-profile'),
	]