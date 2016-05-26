#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseKadaAuthentication
from tastypie import fields
from core.models import Service
from core.api.user import UserResource

class ServiceResource(KadaResource):
    author = fields.ToOneField(UserResource, 'author', null=True, full=True)
    favourites = fields.ToManyField(UserResource, 'favourites', null=True, full=True)
    likes = fields.ToManyField(UserResource, 'likes', null=True, full=True)
    class Meta:
        queryset = Service.objects.all()
        authentication = BaseKadaAuthentication()