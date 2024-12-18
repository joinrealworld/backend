"""
URL configuration for joinrealworld project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_urls_v1 = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('user.urls.v1')),
    path('api/v1/notifications/', include('notification.urls.v1')),
    path('api/v1/channel/', include('channel.urls.v1')),
    path('api/v1/payment/', include('payment.urls.v1')),
    path('api/v1/polls/', include('polls.urls.v1')),
    path('api/v1/checklist/', include('checklist.urls.v1')),
    # path('api/v1/streams/', include('streams.urls.v1')),
    path('api/v1/blackhall/', include('blackhall.urls.v1')),
    path('api/v1/content/', include('content.urls.v1')),
    path('api/v1/media/', include('media_channel.urls.v1')),
    path('api/v1/feedback/', include('feedback.urls.v1')),
    path('api/v1/support/', include('support.urls.v1')),
    path('api/v1/clan/', include('clan.urls.v1')),
    path('api/v1/raffel/', include('raffel.urls.v1')),
    path('api/v1/quiz/', include('quiz.urls.v1')),
]

urlpatterns = app_urls_v1

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)