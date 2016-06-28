#!/usr/bin/python
# -*- coding: utf-8 -*-
"""URL Configuration
# APIs
所有的API URL都在这里定义
"""

# Django Modules
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^core/', include(admin.site.urls)),                                       # Django Admin
]