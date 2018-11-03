from django.urls import path
from .views import news_detail, up_token, AddNewsCommentView, comment_new

app_name = 'news'
urlpatterns = [
    path('news_detail/<int:news_id>', news_detail, name='news_detail'),
    path('up-token/', up_token, name='up_token'),
    path('add-comment/', AddNewsCommentView.as_view(), name='add_comment'),
    path('comment/', comment_new, name='comment_news'),
]

