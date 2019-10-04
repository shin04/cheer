from rest_framework import serializers
from .models import Post, Comment
from accounts.models import CustomUser as User
from .forms import SignUpForm

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'created_date', 'published_date', 'pk')

    def create(self, validated_data):
        user_data = validated_data.pop('author')
        user = User.objects.get(username=user_data['username'])
        post = Post.objects.create(author=user, **validated_data)
        return post

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    class Meta:
        model = Comment
        fields = ('post', 'author', 'text', 'created_date')
