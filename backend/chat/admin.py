from django.contrib import admin

# Register your models here.
from chat.models import Group, Chat

admin.site.register(Group)
admin.site.register(Chat)