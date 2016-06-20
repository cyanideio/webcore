#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from core.utils.resource import BaseResource
from core.utils.auth import MessageAuthorization, BaseAuthentication
from core.api.user import UserResource
from core.models import Message
from kada.models import Gallery

class MessageResource(BaseResource):
    author = fields.ToOneField(UserResource, 'author', null=True, full=True)
    target = fields.ToOneField(UserResource, 'target', null=True, full=True)
    class Meta:
        filtering = {
            'msg_type':('exact')
        } 
        queryset = Message.objects.all()
        authentication = BaseAuthentication()
        authorization = MessageAuthorization()

    def dehydrate(self, bundle):
    	if bundle.data['msg_type'] in [1,0]:
    		target_id = int(bundle.data['jump_target'])
    		name = Gallery.objects.get(id=target_id).name
    		bundle.data['name'] = name
        return bundle