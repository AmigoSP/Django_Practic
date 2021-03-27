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
        fields = ('body', )
