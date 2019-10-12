from rest_framework import serializers
from .models import Post, Comment
from accounts.models import CustomUser as User
from .forms import SignUpForm

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Post
        fields = ('id', 'author', 'author_id', 'title', 'text', 'created_date', 'published_date', 'achievement')

    def create(self, validated_date):
        validated_date['author'] = validated_date.get('author_id', None)
        if validated_date['author'] is None:
            raise serializers.ValidationError("user not found.")
        del validated_date['author_id']

        return Post.objects.create(**validated_date)

    def update(self, instance, validated_date):
        instance.title = validated_date.get('title', instance.title)
        instance.text = validated_date.get('text', instance.text)
        instance.published_date = validated_date.get('published_date', instance.published_date)
        instance.achievement = validated_date.get('achievement', instance.achievement)
        instance.save()

        return instance

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'post', 'post_id', 'author', 'text', 'created_date')

    def create(self, validated_date):
        validated_date['post'] = validated_date.get('post_id', None)
        if validated_date['post'] is None:
            raise serializers.ValidationError("post not found.")
        del validated_date['post_id']

        return Comment.objects.create(**validated_date)
