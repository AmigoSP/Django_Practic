from django.urls import path

from .views import index, RegisterUserView, logout_view, LoginUserView, user_profile, messages_main


# app_name = 'accounts'
urlpatterns = [
    path('accounts/profile/messages/', messages_main, name='messages_main'),
    path('accounts/profile/', user_profile, name='user_profile'),
    path('accounts/login/', LoginUserView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('', index, name='index'),
]
