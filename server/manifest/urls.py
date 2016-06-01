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

# Core APIs
from core.api.friend import FriendResource
from core.api.message import MessageResource
from core.api.user import UserProfileResource
from core.api.user import UserResource

# Kada APIs
from kada.api.advertise import AdvertiseResource
from kada.api.comment import CommentResource
from kada.api.feedback import FeedbackResource
from kada.api.gallery import GalleryResource
from kada.api.scene import SceneResource
from kada.api.scene_set import SceneSetResource
from kada.api.service import ServiceResource

# Custom APIs
from core.auth.api import login, register, verify
from kada.api.gallery_post import gallery_post

v_api = Api(api_name=API_V_STRING)

# 在当前的API重注册所有的 CoreResource
v_api.register(UserProfileResource())
v_api.register(UserResource())
v_api.register(FriendResource())
v_api.register(MessageResource())

# 在当前的API重注册所有的 KadaResource
v_api.register(AdvertiseResource())
v_api.register(CommentResource())
v_api.register(FeedbackResource())
v_api.register(GalleryResource())
v_api.register(SceneResource())
v_api.register(SceneSetResource())
v_api.register(ServiceResource())

urlpatterns = [
	url(r'^login/', login, name='login'), 			    						# Custom.Login API
	url(r'^register/', register, name='register'), 	    						# Custom.Register API
	url(r'^verify/', verify, name='verify'), 									# Custom.Verify API
	url(r'^kada/api/gallery_post', gallery_post, name='gallery_post'), 			# Custom.Verify API
    url(r'^api/', include(v_api.urls)),				    						# Tastypie APIs
    url(r'^admin/', include(admin.site.urls)),   	    						# Django Admin
]