from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.list import MultipleObjectMixin

from myblog.models.post import Post
from myblog.views.post_list import order_by


class PostView(DetailView, MultipleObjectMixin):
    model = Post  # for DetailView
    template_name = 'myblog/post.html'

    paginate_by = 5  # for MultipleObjectMixin

    # cannot define get_queryset for MultipleObjectMixin

    def get_ordering(self):
        return order_by(self.request.GET.get('order_by'))

    def get_context_data(self, **kwargs):
        object_list = Post.objects.get(pk=self.kwargs['pk']).comment_set.order_by(self.get_ordering())
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'myblog/create_post.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'myblog/create_post.html'
    login_url = reverse_lazy('login')

    def test_func(self):
        return Post.objects.get(id=self.kwargs['pk']).user == self.request.user


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'myblog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:feed')
    login_url = reverse_lazy('login')

    def test_func(self):
        return Post.objects.get(id=self.kwargs['pk']).user == self.request.user
