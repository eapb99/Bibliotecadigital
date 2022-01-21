from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id']


admin.site.register(User,UserAdmin)

