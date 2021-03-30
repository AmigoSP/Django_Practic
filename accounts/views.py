from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from article.models import Article
from .models import RegisterUser
from .forms import RegisterUserForm


# Create your views here.

def index(request):
    return render(request, 'accounts/index.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def user_profile(request):
    articles = Article.objects.filter(author=request.user.id)
    return render(request, 'accounts/profile.html', {'articles': articles})


class RegisterUserView(CreateView):
    template_name = 'accounts/register.html'
    model = RegisterUser
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    redirect_field_name = None
