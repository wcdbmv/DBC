from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

from myblog.models.tag import Tag
from myblog.models.vote import Vote


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tags = models.ManyToManyField(to=Tag, related_name='posts')
    rating = models.SmallIntegerField(default=0)
    votes = GenericRelation(Vote)

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.pk})

    def __str__(self):
        return f'"{self.title}" by {self.user.username}'
