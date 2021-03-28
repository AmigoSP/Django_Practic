from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Article, Comment
from .forms import ArticleAddForm, CommentAddForm, CommentChangeForm, ArticleChangeForm


def article_main(request):
    articles = Article.objects.all()
    content = {'articles': articles}
    return render(request, 'article/article_main.html', content)


class ArticleAddView(LoginRequiredMixin, CreateView):
    template_name = 'article/article_add.html'
    success_url = reverse_lazy('article_main')
    model = Article
    form_class = ArticleAddForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('article_main'))
        raise ValidationError('Проверьте введенные данные')


class ArticleChangeView(LoginRequiredMixin, UpdateView):
    template_name = 'article/article_change.html'
    model = Article
    form_class = ArticleChangeForm
    success_url = reverse_lazy('article_main')

    def get_object(self, queryset=None):
        return Article.objects.get(pk=self.kwargs['article_id'])


class CommentAddView(LoginRequiredMixin, CreateView):
    template_name = 'article/comment_add.html'
    success_url = reverse_lazy('article_main')
    model = Comment
    form_class = CommentAddForm

    def post(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs['article_id']
        form = self.form_class(request.POST or None, user=user, article_id=article_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('article_main'))
        raise ValidationError('Проверьте введенные данные')


class CommentChangeView(LoginRequiredMixin, UpdateView):
    template_name = 'article/comment_change.html'
    model = Comment
    form_class = CommentChangeForm
    success_url = reverse_lazy('article_main')

    def get_object(self, queryset=None):
        return Comment.objects.get(pk=self.kwargs['comment_id'])
