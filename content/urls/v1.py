from django.urls import path, include
from content import views

urlpatterns = [
    path("upload", views.UploadContentView.as_view(), name='content'),
]