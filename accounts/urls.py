from django.urls import path

from .views import index, RegisterUserView, logout_view, LoginUserView


# app_name = 'accounts'
urlpatterns = [
    path('accounts/login/', LoginUserView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('', index, name='index'),
]
