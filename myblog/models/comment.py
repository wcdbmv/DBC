from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from myblog.models.post import Post
from myblog.models.vote import Vote


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    votes = GenericRelation(Vote)

    def __str__(self):
        return f'"{self.body[:20]}..." on {self.post.title} by {self.user.username}'
