from django.db import models
from django.urls import reverse

from myblog.managers.ordered import OrderedQuerySet


class Tag(models.Model):
    tag = models.SlugField(unique=True)
    objects = OrderedQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'tag': self.tag})

    def __str__(self):
        return f'{self.tag}'
