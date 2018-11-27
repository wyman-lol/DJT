from django.urls import path
from .views import *

app_name = 'course'
urlpatterns = [
    path('index/', index_view, name='index_view'),
    path('course/', course, name='course'),
    path('course-detail/<int:course_id>/', course_detail, name='course_detail'),
    path('token/', course_token, name='course_token'),
]