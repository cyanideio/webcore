#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from kada.utils.resource import KadaResource
from kada.utils.auth import MessageAuthorization, BaseKadaAuthentication
from core.api.user import UserResource
from core.models import Message

class MessageResource(KadaResource):
    author = fields.ToOneField(UserResource, 'author', null=True, full=True)
    target = fields.ToOneField(UserResource, 'target', null=True, full=True)
    class Meta:
        queryset = Message.objects.all()
        authentication = BaseKadaAuthentication()
        authorization = MessageAuthorization()