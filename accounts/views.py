from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from article.models import Article
from .models import RegisterUser, PrivateMessage
from .forms import RegisterUserForm

# Create your views here.
from .utils import HandlerPrivateMessages


def index(request):
    return render(request, 'accounts/index.html')


@login_required
def messages_main(request):
    user = request.user.id
    messages = PrivateMessage.objects.filter(Q(from_user__id=user) | Q(to_user__id=user))
    content = HandlerPrivateMessages(messages, main_user_id=user).get_all_user_chats
    return render(request, 'accounts/private_messages.html', content)


@login_required
def message_detail(request):
    main_user = request.user.id
    secondary_user = request.GET.get('user_id')
    secondary_username = request.GET.get('username')
    chats = PrivateMessage.objects.filter(
        (Q(from_user__id=main_user) & Q(to_user__id=secondary_user)) |
        (Q(from_user__id=secondary_user) & Q(to_user__id=main_user)))
    content = HandlerPrivateMessages(chats, main_user_id=main_user, secondary_user_id=secondary_user,
                                     secondary_username=secondary_username).get_chat_with_user
    return render(request, 'accounts/private_message_detail.html', content)


@login_required
def message_all_unread(request):
    user = request.user.id
    unread_messages = HandlerPrivateMessages.get_unread_messages(user, only_messages=True).get_all_user_chats
    return render(request, 'accounts/private_messages.html', unread_messages)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def user_profile(request):
    articles = Article.objects.filter(author=request.user.id)
    unread_messages = HandlerPrivateMessages.get_unread_messages(request.user.id).count_unread
    return render(request, 'accounts/profile.html', {'articles': articles, 'unread_messages': unread_messages})


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
