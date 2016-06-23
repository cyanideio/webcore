#!/usr/bin/python
# -*- coding: utf-8 -*-
"""URL Configuration
# APIs
所有的API URL都在这里定义
"""

API_VERSION = 1
API_V_STRING = "v%s" % API_VERSION

# Django Modules
from django.conf.urls import include, url
from django.contrib import admin

# Third Party Modules
from tastypie.api import Api

# Core APIs
from core.api.friend import FriendResource
from core.api.message import MessageResource
from core.api.user import UserProfileResource
from core.api.user import UserResource
from core.api.tags import TagResource

# Custom APIs
from core.auth.api import login, register, verify
from core.api.friend_toggle import friend_toggle

v_api = Api(api_name=API_V_STRING)

# 在当前的API重注册所有的 CoreResource
v_api.register(UserProfileResource())
v_api.register(UserResource())
v_api.register(FriendResource())
v_api.register(MessageResource())
v_api.register(TagResource())

urlpatterns = [
    url(r'^login/', login, name='login'),                                           # Custom.Login API
    url(r'^register/', register, name='register'),                                  # Custom.Register API
    url(r'^verify/', verify, name='verify'),                                        # Custom.Verify API
    url(r'^friend_toggle/', friend_toggle, name='friend_toggle'),                   # Custom.Verify API
    url(r'^api/', include(v_api.urls)),                                             # Tastypie APIs
    url(r'^admin/', include(admin.site.urls)),                                      # Django Admin
]