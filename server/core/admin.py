#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from core.models import Friend, Message, UserProfile
from django.contrib.auth.admin import UserAdmin

class CommonAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated')

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    list_display = ('nickname', 'is_active', 'date_joined', 'is_staff', 'email')
    inlines = [ UserProfileInline, ]
    def nickname(self, obj):
        return UserProfile.objects.get(user=obj).nickname


admin.site.register(User, UserProfileAdmin)

admin.site.register(Friend, CommonAdmin)
admin.site.register(Message, CommonAdmin)
# admin.site.register(UserProfile, CommonAdmin)