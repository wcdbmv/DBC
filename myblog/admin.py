from django.contrib import admin

from myblog.models.comment import Comment
from myblog.models.post import Post

admin.site.register(Post)
admin.site.register(Comment)
