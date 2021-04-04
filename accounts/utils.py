from django.db.models import Q

from .models import PrivateMessage


class HandlerPrivateMessages:

    def __init__(self, messages, main_user_id=None, secondary_user_id=None, secondary_username=None,
                 count_unread=0):
        self.messages = messages
        self.main_user_id = main_user_id
        self.secondary_user_id = secondary_user_id
        self.secondary_username = secondary_username
        self.count_unread = count_unread

    @property
    def get_all_user_chats(self):
        all_chats = set()
        for message in self.messages:
            from_user = message.from_user.get()
            to_user = message.to_user.get()
            if from_user.id is self.main_user_id:
                all_chats.add(to_user)
            else:
                if not message.reading:
                    self.count_unread += 1
                all_chats.add(from_user)
        return {'chats': all_chats, 'unread_messages': self.count_unread, 'new_chats': None}

    @property
    def get_chat_with_user(self):
        chat = {'username': self.secondary_username, 'messages': list()}
        for message in self.messages:
            value = {'username': message.from_user.get().username, 'body': message.body, 'date': message.date}
            chat['messages'].append(value)
            if message.from_user.get().id is not self.main_user_id:
                message.reading = True
                message.save()
        content = {'chats': chat,
                   'unread_messages': HandlerPrivateMessages.get_unread_messages(self.main_user_id).count_unread}
        return content

    @classmethod
    def get_unread_messages(cls, user, only_messages=False):
        unread_messages = PrivateMessage.objects.filter(Q(to_user__id=user)).filter(
            reading=False)
        if only_messages:
            return cls(messages=unread_messages, main_user_id=user)
        count_unread = unread_messages.count()
        return cls(count_unread=count_unread, messages=unread_messages, main_user_id=user)
