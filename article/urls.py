from django.urls import path

from .views import article_main, ArticleAddView, CommentAddView


# app_name = 'article'
urlpatterns = [
    path('', article_main, name='article_main'),
    path('add/', ArticleAddView.as_view(), name='article_add'),
    path('<int:article_id>/comment/add/', CommentAddView.as_view(), name='comment_add')
]