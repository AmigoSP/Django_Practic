from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from article.models import Article
from .models import RegisterUser, PrivateMessage
from .forms import RegisterUserForm


# Create your views here.

def index(request):
    return render(request, 'accounts/index.html')


@login_required
def messages_main(request):
    user = request.user
    all_chats = set()
    messages = PrivateMessage.objects.filter(Q(from_user__id=user.id) | Q(to_user__id=user.id))
    for message in messages:
        from_user = message.from_user.get()
        to_user = message.to_user.get()
        if from_user.id is user.id:
            all_chats.add(to_user)
        else:
            all_chats.add(from_user)
    return render(request, 'accounts/private_messages.html', {'chats': all_chats})


@login_required
def message_detail(request):
    chat = {}
    main_user = request.user.id
    secondary_user = request.GET.get('user_id')
    secondary_username = request.GET.get('username')
    chat['username'] = secondary_username
    chat['messages'] = list()
    chats = PrivateMessage.objects.filter(
        (Q(from_user__id=main_user) & Q(to_user__id=secondary_user)) |
        (Q(from_user__id=secondary_user) & Q(to_user__id=main_user)))
    for message in chats:
        value = {'username': message.from_user.get().username, 'body': message.body, 'date': message.date}
        chat['messages'].append(value)
    content = {'chats': chat}
    return render(request, 'accounts/private_message_detail.html', content)


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
