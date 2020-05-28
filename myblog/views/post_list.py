from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from myblog.models.post import Post


def order_by(order):
    if order in ('rating', '-rating', 'pub_date'):
        return order
    return '-pub_date'


class FeedView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 5

    def get_queryset(self):
        order = order_by(self.request.GET.get('order_by'))
        return Post.objects.order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BlogView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        self.kwargs['first_name'] = user.first_name
        self.kwargs['last_name'] = user.last_name
        order = order_by(self.request.GET.get('order_by'))
        return Post.objects.filter(user=user).order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_name'] = self.kwargs['first_name']
        context['last_name'] = self.kwargs['last_name']
        return context


class TagView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(tags__tag=self.kwargs['tag']).order_by(order_by(self.request.GET.get('order_by')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context
