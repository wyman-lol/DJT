from django.urls import path
from .views import news_detail, up_token, AddNewsCommentView, comment_new, news_list, news_tag_list, news_with_tag

app_name = 'news'
urlpatterns = [
    path('news_detail/<int:news_id>', news_detail, name='news_detail'),
    path('up-token/', up_token, name='up_token'),
    path('add-comment/', AddNewsCommentView.as_view(), name='add_comment'),
    path('comment/', comment_new, name='comment_news'),
    path('list/', news_list, name='news_list'),
    path('tag/list/', news_tag_list, name='news_tag_list'),
    path('news-with-tag/', news_with_tag, name='news_with_tag'),
]

