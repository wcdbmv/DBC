from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from myblog.models.comment import Comment
from myblog.models.article import Article


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    template_name = 'myblog/create.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article = Article.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:articles', kwargs={'pk': self.kwargs['pk']})


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'myblog/create.html'
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('blog:articles', kwargs={'pk': Comment.objects.get(id=self.kwargs['pk']).article_id})


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'myblog/confirm_delete.html'
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('blog:articles', kwargs={'pk': Comment.objects.get(id=self.kwargs['pk']).article_id})
