from django.urls import path
from . import views
from .views import (UserViewSet, PostViewSet, CommentViewSet,
                    MyPostViewSet, PostCommentViewSet, UserCommentViewSet)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'myposts', MyPostViewSet, base_name='MyPost')
router.register(r'postcomment', PostCommentViewSet, basename='PostComment')
router.register(r'usercomment', UserCommentViewSet, base_name='UserComment')

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('mypost/', views.my_post_list, name='my_post_list'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/achive/', views.post_achieve, name='post_achieve'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('signup/', views.signup, name='signup'),

    path('api/who', views.is_user, name='who'),
]
