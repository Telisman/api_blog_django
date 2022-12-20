from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post,Category

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username','posts']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category']

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner','category']




