from django.urls import path

from .views import article_main, ArticleAddView, CommentAddView, CommentChangeView, ArticleChangeView


# app_name = 'article'
urlpatterns = [
    path('', article_main, name='article_main'),
    path('add/', ArticleAddView.as_view(), name='article_add'),
    path('<int:article_id>/comment/add/', CommentAddView.as_view(), name='comment_add'),
    path('<int:article_id>/change/', ArticleChangeView.as_view(), name='article_change'),
    path('comment/change/<int:comment_id>/', CommentChangeView.as_view(), name='comment_change')
]