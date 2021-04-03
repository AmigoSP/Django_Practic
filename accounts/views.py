from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from article.models import Article
from .models import RegisterUser, PrivateMessage, ChatsFromUsers
from .forms import RegisterUserForm, PrivateMessageAdd

# Create your views here.
from .utils import HandlerPrivateMessages


def index(request):
    return render(request, 'accounts/index.html')


@login_required
def search_user_for_message(request):
    chats = set()
    new_chats = set()
    secondary_username = request.GET.get('secondary_username')
    main_user = request.user
    if secondary_username:
        search_users_secondary = User.objects.filter(username__icontains=secondary_username).exclude(
            username=main_user.username)
        if search_users_secondary:
            try:
                main_user_chat = ChatsFromUsers.objects.get(main_user=main_user)
            except ChatsFromUsers.DoesNotExist:
                all_main_user_chats = None
            else:
                all_main_user_chats = main_user_chat.chats_from_users.all()
            for user in search_users_secondary:
                if all_main_user_chats and user not in all_main_user_chats:
                    new_chats.add(user)
                chats.add(user)
            unread_messages = HandlerPrivateMessages.get_unread_messages(main_user.id).count_unread
            full_content = {'chats': chats, 'new_chats': new_chats, 'unread_messages': unread_messages}
            return render(request, 'accounts/private_messages.html', full_content)
        else:
            return render(request, 'accounts/private_messages.html', {'not_found': "Users not found"})


class MessageAddView(LoginRequiredMixin, CreateView):
    template_name = 'accounts/private_message_add.html'
    model = PrivateMessage
    form_class = PrivateMessageAdd
    success_url = reverse_lazy('messages_main')

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        return render(self.request, 'accounts/private_message_add.html', {'form': form})


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
