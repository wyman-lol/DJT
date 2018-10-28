from django.urls import path
from .views import news_detail

app_name = 'news'
urlpatterns = [
    path('news_detail/<int:news_id>', news_detail, name='news_detail'),
]

