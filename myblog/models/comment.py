from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from myblog.models.article import Article
from myblog.models.vote import Vote


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    votes = GenericRelation(Vote)

    def __str__(self):
        return f'"{self.body[:20]}..." on {self.article.title} by {self.user.username}'
