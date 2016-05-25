#!/usr/bin/python
# -*- coding: utf-8 -*-
"""kada URL Configuration
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

# APIs
from core.api.friend import FriendResource
from core.api.advertise import AdvertiseResource
from core.api.comment import CommentResource
from core.api.feedback import FeedbackResource
from core.api.gallery import GalleryResource
from core.api.message import MessageResource
from core.api.scene import SceneResource
from core.api.scene_template import SceneTemplateResource
from core.api.service import ServiceResource

# Custom APIs
from core.auth.api import login, register, verify

v_api = Api(api_name=API_V_STRING)

# 在当前的API重注册所有的 Resource
v_api.register(FriendResource())
v_api.register(AdvertiseResource())
v_api.register(CommentResource())
v_api.register(FeedbackResource())
v_api.register(GalleryResource())
v_api.register(MessageResource())
v_api.register(SceneResource())
v_api.register(SceneTemplateResource())
v_api.register(ServiceResource())

urlpatterns = [
	url(r'^login/', login, name='login'), 			# Custom.Login API
    url(r'^api/', include(v_api.urls)),				# Tastypie APIs
    url(r'^admin/', include(admin.site.urls)),   	# Django Admin
]