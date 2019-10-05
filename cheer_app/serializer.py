from rest_framework import serializers
from .models import Post, Comment
from accounts.models import CustomUser as User
from .forms import SignUpForm

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        #extra_kwargs = { 'username': { 'read_only': False } }

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Post
        fields = ('id', 'author', 'author_id', 'title', 'text', 'created_date', 'published_date')

    def create(self, validated_date):
        validated_date['author'] = validated_date.get('author_id', None)

        if validated_date['author'] is None:
            raise serializers.ValidationError("user not found.")

        del validated_date['author_id']

        return Post.objects.create(**validated_date)

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_date')
