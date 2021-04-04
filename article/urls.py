from django.urls import path

from .views import article_main, \
    ArticleAddView, \
    CommentAddView, \
    CommentChangeView, \
    ArticleChangeView, \
    article_detail, article_search



# app_name = 'article'
urlpatterns = [
    path('', article_main, name='article_main'),
    path('add/', ArticleAddView.as_view(), name='article_add'),
    path('search/', article_search, name='article_search'),
    path('<int:article_id>/', article_detail, name='article_detail'),
    path('<int:article_id>/comment/add/', CommentAddView.as_view(), name='comment_add'),
    path('<int:article_id>/change/', ArticleChangeView.as_view(), name='article_change'),
    path('comment/change/<int:comment_id>/', CommentChangeView.as_view(), name='comment_change')
]