from myblog.managers.ordered import OrderedQuerySet


class ArticleQuerySet(OrderedQuerySet):
    def tags(self, tag):
        return self.filter(tags__tag=tag)

    def users(self, user):
        return self.filter(user=user)

    def comments(self, article_id):
        return self.get(id=article_id).comment_set
