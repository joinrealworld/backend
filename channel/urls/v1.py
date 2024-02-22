from django.urls import path, include
from rest_framework import routers
from channel import views

urlpatterns = [
    path('fetch/category', views.FetchCategoryAPIView.as_view(), name='fetch-category'),
    path('fetch/course/<int:category_id>', views.FetchCourseCategoryAPIView.as_view(), name='fetch-course-category'),
    path('fetch/course/<int:course_id>/data', views.FetchCourseDataAPIView.as_view(), name='fetch-course-data'),
    path('fetch/course/<int:course_id>/quiz/<int:quiz_index>', views.FetchCourseQuizAPIView.as_view(), name='fetch-course-quiz'),
    path('add/favourite/content', views.AddFavouriteContentAPIView.as_view(), name='add-favourite-content'),
    path('remove/favourite/content', views.RemoveFavouriteContentAPIView.as_view(), name='remove-favourite-content'),
    path('add/favourite/course', views.AddFavouriteCourseAPIView.as_view(), name='add-favourite-course'),
    path('remove/favourite/course', views.RemoveFavouriteCourseAPIView.as_view(), name='remove-favourite-course'),
    path('mark/complete/course', views.MarkCompleteContentAPIView.as_view(), name='mark-complete-content'),
	]