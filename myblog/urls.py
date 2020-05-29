from django.urls import path

from myblog.models.comment import Comment
from myblog.models.post import Post
from myblog.views.comment import CommentCreate
from myblog.views.post import PostView, PostCreate, PostUpdate, PostDelete
from myblog.views.post_list import FeedView, BlogView, TagView
from myblog.views.vote import VoteView

app_name = 'blog'
urlpatterns = [
    # ex: /blog/feed/
    path('feed/', FeedView.as_view(), name='feed'),
    # ex: /blog/user/wcdbmv
    path('user/<str:username>', BlogView.as_view(), name='user_posts'),
    # ex: /blog/post/5/
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    # ex: /blog/post/5/upvote
    path('post/<int:pk>/upvote', VoteView.as_view(model=Post, vote_value=1), name='post_upvote'),
    # ex: /blog/post/5/downvote
    path('post/<int:pk>/downvote', VoteView.as_view(model=Post, vote_value=-1), name='post_downvote'),
    # ex: /blog/post/create/
    path('post/create/', PostCreate.as_view(), name='create_post'),
    # ex: /blog/post/5/update
    path('post/create/<int:pk>/update', PostUpdate.as_view(), name='update_post'),
    # ex: /blog/post/5/delete
    path('post/<int:pk>/delete', PostDelete.as_view(), name='delete_post'),
    # ex: /blog/post/5/comment/
    path('post/<int:pk>/comment/', CommentCreate.as_view(), name='create_comment'),
    # ex: /blog/tag/job
    path('tag/<str:tag>/', TagView.as_view(), name='tag'),
    # ex: /blog/comment/15/upvote
    path('comment/<int:pk>/upvote', VoteView.as_view(model=Comment, vote_value=1), name='post_upvote'),
    # ex: /blog/comment/15/downvote
    path('comment/<int:pk>/downvote', VoteView.as_view(model=Comment, vote_value=-1), name='post_downvote'),
]
