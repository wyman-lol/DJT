from rest_framework import serializers
from .models import NewsComment, News, NewsHot
from ..admin_staff.models import NewsTag
from ..account.serializers import UserSerializers


# 序列化模型
class NewsCommentSerializers(serializers.ModelSerializer):
    # 序列化author
    author = UserSerializers()

    class Meta:
        # 要序列化的模型
        model = NewsComment
        # 要序列化的字段
        # fields = '__all__'序列化全部
        fields = ('id', 'content', 'create_time', 'author')


class NesTagSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = '__all__'


class NewsSerializers(serializers.ModelSerializer):
    author = UserSerializers()
    tag = NesTagSerializers()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'photo_url', 'add_time', 'author', 'tag')


class NewsHotSerializer(serializers.ModelSerializer):
    news = NewsSerializers()

    class Meta:
        model = NewsHot
        # fields的字段必须要有而且一致
        fields = ('id', 'priority', 'is_delete', 'news')
