from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Article, Comment
from .forms import ArticleAddForm, CommentAddForm, CommentChangeForm, ArticleChangeForm


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    return render(request, 'article/article_detail.html', {'article': article})


def article_search(request):
    input_data = request.GET.get('search_form')
    articles = Article.objects.filter(Q(title__icontains=input_data) | Q(body__icontains=input_data))
    if articles:
        return render(request, 'article/article_main.html', {'articles': articles, 'result_found': 'Результат поиска:'})
    return render(request, 'article/article_main.html', {'result_found': 'По Вашему запросу ничего не найдено'})


def article_main(request):
    articles = Article.objects.all().order_by('-date')
    pages = Paginator(articles, 15)
    page_number = request.GET.get('page', 1)
    page_obj = pages.get_page(page_number)
    content = {'page_obj': page_obj}
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
