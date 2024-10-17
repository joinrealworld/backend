from django.urls import path, include
from rest_framework import routers
from user import views

urlpatterns = [
    path('login', views.LoginWithPasswordAPIView.as_view(), name='login-with-password'),
    path('signup', views.SignUpAPIViewAPIView.as_view(), name='sign-up'),
    path('verify_email', views.VerifyEmailAPIView.as_view(), name='verify-email'),
    path('resend_mail', views.SendVerificationMailAPIView.as_view(), name='resend-email'),
    path('forgot_password', views.ForgotPasswordAPIView.as_view(), name='forgot-email'),
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
    path('change/authentication', views.ChangeAuthenticationAPIView.as_view(), name='change-authentication'),
    path('check/email', views.CheckEmailAPIView.as_view(), name='check-email-api-exists'),
    path('purches/identity_booster', views.PurchaseIdentityBoosterAPIView.as_view(), name='purches-ib'),
    path('purches/tune', views.PurchesTuneAPIView.as_view(), name='purches-tune'),
    path('fetch/purchesed/emoji', views.ListMyEmojiAPIView.as_view(), name='list-my-emoji'),
    path('fetch/purchesed/tune', views.ListMyTuneAPIView.as_view(), name='list-my-tune'),
    path('fetch/wallpapers', views.FetchWallPapaerAPIView.as_view(), name='list-wallpaper'),
    path('buy/wallpapers', views.BuyWallPapaerAPIView.as_view(), name='buy-wallpaper'),
    path('change/wallpaper', views.ChangeWallPapaerAPIView.as_view(), name='change-wallpaper'),
    path('change/tune', views.ChangeTuneAPIView.as_view(), name='change-tune'),
    path('change/emoji', views.ChangeEmojiAPIView.as_view(), name='change-emoji'),
    path('set/offline', views.SetOfflineAPIView.as_view(), name='set-offline'),
    path('list/tune', views.ListTuneAPIView.as_view(), name='list-tune'),
    path('list', views.UserListAPIView.as_view(), name='user-list'),
    path('change/ai_pic', views.ChangeAIPicAPIView.as_view(), name='change-ai-pic'),
	]