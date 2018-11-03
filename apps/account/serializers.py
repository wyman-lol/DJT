from rest_framework import serializers
from .models import User


# 序列化模型
class UserSerializers(serializers.ModelSerializer):
    class Meta:

        model = User

        # fields = '__all__'
        fields = ('id', 'username')