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
    path('change_username', views.ChangeUserNameAPIView.as_view(), name='change-username'),
    path('change_password', views.ChangePasswordAPIView.as_view(), name='change-password'),
    path('change_status', views.ChangeStatusAPIView.as_view(), name='change-status'),
    path('change_invisible', views.ChangeInvisibleAPIView.as_view(), name='change-invisible'),
    path('change_avatar', views.ChangeAvatarAPIView.as_view(), name='change-avatar'),
    path('change_background', views.ChangeBackgroundAPIView.as_view(), name='change-background'),
    path('change_bio', views.ChangeBioAPIView.as_view(), name='change-bio'),
    path('logout', views.SingleDeviceLogoutAPIView.as_view(), name='sigle-device-logout'),
    path('all_logout', views.AllDeviceLogoutAPIView.as_view(), name='all-devices-logout'),
    path('feedback', views.UserFeedbackAPIView.as_view(), name='user-feedback'),
    path('theme', views.UpdateThemeAPIView.as_view(), name='update-theme'),
    path('sound_effect', views.UpdateSoundEffectAPIView.as_view(), name='sound-effect'),
	]