from django.urls import path
from .views import *

app_name = 'course'
urlpatterns = [
    path('index/', index_view, name='index_view'),
    path('course/', course, name='course'),
]