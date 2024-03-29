#!/usr/bin/python
# -*- coding: utf-8 -*-
API_VERSION = 1
API_V_STRING = "v%s" % API_VERSION

# Django Modules
from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.contrib import admin

# Third Party Modules
from tastypie.api import Api

# Custom Error Handlers
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

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
    url(r'^fans/', friend_toggle, name='friend_toggle'),                            # Custom.Friends API
    url(r'^api/', include(v_api.urls)),                                             # Tastypie APIs
]