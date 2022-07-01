from django.contrib import admin
from .models import Item, Borrowed_item
from django.contrib.auth.models import Group
# Register your models here.

admin.site.register(Item)
admin.site.unregister(Group)
admin.site.register(Borrowed_item)