from rest_framework import serializers
from .models import NewsComment
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