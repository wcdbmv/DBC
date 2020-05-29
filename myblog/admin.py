from django.contrib import admin

from myblog.models.article import Article
from myblog.models.comment import Comment
from myblog.models.tag import Tag

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Tag)
