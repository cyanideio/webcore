#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseKadaAuthentication, FriendsAuthorization
from core.api.user import UserResource
from core.models import Friend

class FriendFollowerResource(KadaResource):
    verify_keys = ['follower']
    follower = fields.ToOneField(UserResource, 'follower', null=True, full=True)
    class Meta:
        resource_name = 'friend/follows'
        queryset = Friend.objects.all()
        authentication = BaseKadaAuthentication()
        authorization = FriendsAuthorization('follows')
        filtering = {
            'follower':('exact'),
        }


class FriendFolloweeResource(KadaResource):
    verify_keys = ['followee']
    followee = fields.ToOneField(UserResource, 'followee', null=True, full=True)
    class Meta:
        resource_name = 'friend/fans'
        queryset = Friend.objects.all()
        authentication = BaseKadaAuthentication()
        authorization = FriendsAuthorization('fans')
        filtering = {
            'followee':('exact'),
        }