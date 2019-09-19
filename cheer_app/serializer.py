from rest_framework import serializers
from .models import Post, Comment
from accounts.models import CustomUser as User
from .forms import SignUpForm

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

        def create(self, validated_data):
          """
          passwordをハッシュ化してから登録(djangoデフォルトのライブラリを使用)
          """
          password = validated_data.get('password')
          validated_data['password'] = make_password(password)
          return User.objects.create(**validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'created_date', 'published_date', 'pk')

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    class Meta:
        model = Comment
        fields = ('post', 'author', 'text', 'created_date', 'approved_comment')
