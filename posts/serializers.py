from django.contrib.auth        import get_user_model
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from .models              import Post


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'nickname', 'email')


class PostSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.nickname')

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('created_at', 'edited_at', 'author', 'id')