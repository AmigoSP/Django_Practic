from django.contrib import admin

# Register your models here.
from .models import PrivateMessage, ChatsFromUsers, RegisterUser

admin.site.register(PrivateMessage)
admin.site.register(ChatsFromUsers)
admin.site.register(RegisterUser)
