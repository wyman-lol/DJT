from django.urls import path
from .views import *

app_name = 'admin_staff'
urlpatterns = [
    path('staff/', staff, name='staff'),
    path('news_manage/', NewsTagView.as_view(), name='news_manage'),
]