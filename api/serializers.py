from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post,Category

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id','username','posts']

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

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields =['username','password','password2']
        extra_kwargs = {
            'password':{'write_only': True }
        }
    def save(self):
        user = User(
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match '})
        user.set_password(password)
        user.save()
        return user