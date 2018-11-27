from django.urls import path
from .views import *
from .course_view import *
from ..news.views import *

app_name = 'admin_staff'
urlpatterns = [
    path('staff/', staff, name='staff'),
    path('news_manage/', NewsTagView.as_view(), name='news_manage'),
    path('newspub/', NewsPUbView.as_view(), name='newspub'),
    path('newsedit/', NewsEditView.as_view(), name='newsedit'),
    path('upload-file/', UploadFile, name='upload_file'),
    path('news-master/', NewsMasterView.as_view(), name='newsmaster'),
    path('news-hot/', NewsHotView.as_view(), name='news_hot'),
    path('news-hot-add/', NewsHotAddView.as_view(), name='news_hot_add'),
    path('news_banner/', NewsBannerView.as_view(), name='news_banner'),
]

# 课堂相关的url
urlpatterns += [
    path('course-pub/', CoursePubView.as_view(), name='course-pub'),
]