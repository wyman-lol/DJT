from django.urls import path
from .views import *
from ..news.views import *

app_name = 'admin_staff'
urlpatterns = [
    path('staff/', staff, name='staff'),
    path('news_manage/', NewsTagView.as_view(), name='news_manage'),
    path('newspub/', NewsPUbView.as_view(), name='newspub'),
    path('upload-file/', UploadFile, name='upload_file'),
    path('news-master/', NewsMasterView.as_view(), name='newsmaster'),
    path('news-hot/', NewsHotView.as_view(), name='news_hot'),
    path('news-hot-add/', NewsHotAddView.as_view(), name='news_hot_add'),
]