#!/usr/bin/python
# -*- coding: utf-8 -*-
"""URL Configuration
# APIs
所有的API URL都在这里定义
"""

# Django Modules
from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.contrib import admin
from filebrowser.sites import site

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

urlpatterns = [
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^core/', include(admin.site.urls)),                                       # Django Admin
]
