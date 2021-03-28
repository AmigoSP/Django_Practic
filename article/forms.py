from django import forms

from .models import Article, Comment
from accounts.models import RegisterUser


class ArticleAddForm(forms.ModelForm):
    title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label='Статья', widget=forms.Textarea(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.user = kwargs.get('user')

    def save(self, commit=True):
        article = super().save(commit=False)
        article.title = self.cleaned_data['title']
        article.body = self.cleaned_data['body']
        article.author = RegisterUser.objects.get(username=self.user)
        article.save()
        return article

    class Meta:
        model = Article
        fields = ('title', 'body',)


class ArticleChangeForm(forms.ModelForm):
    def save(self, commit=True):
        article_change = super().save(commit=False)
        article_change.changed = True
        article_change.save()
        return article_change

    class Meta:
        model = Article
        fields = ('title', 'body',)


class CommentAddForm(forms.ModelForm):
    body = forms.CharField(label='Комментарий', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.user = kwargs.get('user')
        self.article_id = kwargs.get('article_id')
        if self.article_id:
            self.article = Article.objects.get(pk=self.article_id)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.body = self.cleaned_data['body']
        comment.author = RegisterUser.objects.get(username=self.user)
        comment.save()
        self.article.comments.add(comment)
        return comment

    class Meta:
        model = Comment
        fields = ('body',)


class CommentChangeForm(forms.ModelForm):
    def save(self, commit=True):
        comment_change = super().save(commit=False)
        comment_change.changed = True
        comment_change.save()
        return comment_change

    class Meta:
        model = Comment
        fields = ('body',)
