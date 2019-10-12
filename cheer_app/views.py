from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from accounts.models import CustomUser as User
from .forms import PostForm, CommentForm, SignUpForm
from .serializer import PostSerializer, CommentSerializer, UserSerializer
from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.authtoken.models import Token

from django.utils import timezone

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form':form})

def index(request):
    return render(request, 'cheer_app/index.html')

def post_list(request):
    non_achieve_post = Post.objects.filter(achievement=False)
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = non_achieve_post.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'cheer_app/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'cheer_app/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'cheer_app/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'cheer_app/post_edit.html', {'form': form})

@login_required
def my_post_list(request):
    achievement_posts = Post.objects.filter(achievement=True).order_by('created_date')
    non_achieve_posts = Post.objects.filter(achievement=False).order_by('created_date')
    posts = non_achieve_posts.filter(published_date__lte=timezone.now()).order_by('created_date')
    drafts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    #posts = Post.objects.all().order_by('created_date')
    return render(request, 'cheer_app/my_post_list.html', {'posts': posts, 'drafts': drafts, 'achievement_posts': achievement_posts})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'cheer_app/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_achieve(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.achieve()
    return redirect(post_detail, pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'cheer_app/add_comment_to_post.html', {'form': form})

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

# rest-framewark
@api_view(['GET'])
def is_user(request):
    return Response({"id": request.user.id, "username": request.user.username, "email": request.user.email, "token": Token.objects.get_or_create(user=request.user)[0].key})

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # @action(detail=True, methods=['post'])
    # def publish(self, request, pk=None):
    #     # post = Post.objects.filter(pk=pk)
    #     # post.published_date = timezone.now()
    #     # post.save()
    #     post = get_object_or_404(Post, pk=pk)
    #     post.publish()
    #     return Response({'ststus': 'success'})

class MyPostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)

class PostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        param_value = self.request.GET.get("query_param")
        id = int(param_value)
        comments = Comment.objects.filter(post__id=id)
        serializer = CommentSerializer(comments)
        return comments

class UserCommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(post__author=user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # @action(detail=False)
    # def get_comment(self, request):
    #     param_value = request.GET.get("query_param")
    #     id = int(param_value)
    #     print(id)
    #     comments = Comment.objects.filter(post__id=id)
    #     print(comments)
    #     serializer = CommentSerializer(comments)
    #     return Response(serializer.data)
