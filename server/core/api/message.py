#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from core.utils.resource import BaseResource
from core.utils.auth import MessageAuthorization, BaseAuthentication
from core.api.user import UserResource
from core.models import Message

class MessageResource(BaseResource):
    author = fields.ToOneField(UserResource, 'author', null=True, full=True)
    target = fields.ToOneField(UserResource, 'target', null=True)
    class Meta:
        filtering = {
            'msg_type':('exact')
        } 
        excludes = ['target']
        queryset = Message.objects.all()
        authentication = BaseAuthentication()
        authorization = MessageAuthorization()