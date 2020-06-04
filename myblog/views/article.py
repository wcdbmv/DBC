from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.list import MultipleObjectMixin

from myblog.models.article import Article
from myblog.views.article_list import order_by


class ArticleView(DetailView, MultipleObjectMixin):
    model = Article  # for DetailView
    template_name = 'myblog/article.html'

    paginate_by = 5  # for MultipleObjectMixin

    # cannot define get_queryset for MultipleObjectMixin

    def get_ordering(self):
        return order_by(self.request.GET.get('order_by'))

    def get_context_data(self, **kwargs):
        object_list = Article.objects.comments(self.kwargs['pk']).order_by(self.get_ordering())
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'body']
    template_name = 'myblog/create_article.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'body']
    template_name = 'myblog/create_article.html'
    login_url = reverse_lazy('login')


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'myblog/confirm_delete.html'
    success_url = reverse_lazy('blog:feed')
    login_url = reverse_lazy('login')
