#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
# Register your models here.
from core.models import Friend, Message, UserProfile

class CommonAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated')

admin.site.register(Friend, CommonAdmin)
admin.site.register(Message, CommonAdmin)
admin.site.register(UserProfile, CommonAdmin)