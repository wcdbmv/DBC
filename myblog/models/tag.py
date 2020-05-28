from django.db import models
from django.urls import reverse


class Tag(models.Model):
    tag = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'tag': self.tag})

    def __str__(self):
        return f'{self.tag}'
