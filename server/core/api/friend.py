#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseKadaAuthentication, FriendsAuthorization
from core.api.user import UserResource
from core.models import Friend

class FriendResource(KadaResource):
    follower = fields.ToOneField(UserResource, 'follower', null=True, full=True)
    followee = fields.ToOneField(UserResource, 'followee', null=True, full=True)

    class Meta:
        resource_name = 'friend'
        queryset = Friend.objects.all()
        authentication = BaseKadaAuthentication()
        authorization = FriendsAuthorization()
        filtering = {
            'follower':('exact'),
            'followee':('exact'),
        }