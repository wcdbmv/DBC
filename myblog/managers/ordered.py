from django.db import models


class OrderedQuerySet(models.QuerySet):
    def newest(self):
        return self.order_by('-pub_date')

    def oldest(self):
        return self.order_by('pub_date')

    def most_rated(self):
        return self.order_by('-rating')

    def least_rated(self):
        return self.order_by('rating')
