from django.urls import path, include
from rest_framework import routers
from channel import views

urlpatterns = [
    path('fetch/master_category', views.FetchMasterCategoryAPIView.as_view(), name='fetch-master-category'),
    path('fetch/category/<slug:master_category_id>', views.FetchCategoryAPIView.as_view(), name='fetch-category'),
    path('fetch/users/<slug:master_category_id>', views.FetchCategoryUsersAPIView.as_view(), name='fetch-users'),
    path('fetch/course/<uuid:category_id>', views.FetchCourseCategoryAPIView.as_view(), name='fetch-course-category'),
    path('fetch/course/<uuid:course_id>/data', views.FetchCourseDataAPIView.as_view(), name='fetch-course-data'),
    path('fetch/course/<uuid:course_id>/quiz/<int:quiz_index>', views.FetchCourseQuizAPIView.as_view(), name='fetch-course-quiz'),
    path('change/favourite/content', views.AddFavouriteContentAPIView.as_view(), name='add-favourite-content'),
    path('change/favourite/course', views.AddFavouriteCourseAPIView.as_view(), name='add-favourite-course'),
    path('mark/complete/course', views.MarkCompleteContentAPIView.as_view(), name='mark-complete-content'),
    path('fetch/favourite/courses', views.FetchFavouriteCoursesAPIView.as_view(), name='fetch-favourite-courses'),
    path('fetch/inprogress/courses', views.FetchInProgressCoursesAPIView.as_view(), name='fetch-favourite-courses'),
    path('store/last/course/content', views.StoreLastCourseContentAPIView.as_view(), name='store-last-content'),
    path('save/progress/channel', views.SaveProgressChannelAPIView.as_view(), name='save-progress-channel'),
    path('random/button', views.RandomButtonAPIView.as_view(), name='random-button'),
    # path('average/quiz/score', views.AverageQuizScoreAPIView.as_view(), name='average-quizz-score'),
    # path('quiz/fail', views.QuizFailAPIView.as_view(), name='quiz-fail'),
	]