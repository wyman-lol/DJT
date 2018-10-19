from django.urls import path
from .views import *

app_name = 'doc'
urlpatterns = [
    path('search/', search, name='search'),
    path('document/', docDownload, name='doc'),
]