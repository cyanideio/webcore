#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication
from core.api.user import UserResource
from tastypie import fields
from kada.models import Service

class ServiceResource(BaseResource):
    author = fields.ToOneField(UserResource, 'author', null=True, full=True)
    favourites = fields.ToManyField(UserResource, 'favourites', null=True, full=True)
    likes = fields.ToManyField(UserResource, 'likes', null=True, full=True)
    class Meta:
        queryset = Service.objects.all()
        authentication = BaseAuthentication()