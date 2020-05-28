from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from myblog.models.post import Post


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs.get('username', '')
        if username:
            user = get_object_or_404(User, username=username)
            self.first_name = user.first_name
            self.last_name = user.last_name
            post_list = Post.objects.filter(user=user)
        else:
            self.first_name = ''
            self.last_name = ''
            post_list = Post.objects.all()
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_name'] = self.first_name
        context['last_name'] = self.last_name
        return context
