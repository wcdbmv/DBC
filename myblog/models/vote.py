from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Vote(models.Model):
    VALUES = (
        ('UP', 1),
        ('DOWN', -1),
    )
    value = models.SmallIntegerField(choices=VALUES)
    user = models.ForeignKey(User, related_name='voter', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
