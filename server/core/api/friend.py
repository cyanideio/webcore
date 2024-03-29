#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication, FriendsAuthorization
from core.api.user import UserResource
from core.models import Friend

class FriendResource(BaseResource):
    follower = fields.ToOneField(UserResource, 'follower', null=True, full=True)
    followee = fields.ToOneField(UserResource, 'followee', null=True, full=True)

    class Meta:
        resource_name = 'friend'
        queryset = Friend.objects.all()
        authentication = BaseAuthentication()
        authorization = FriendsAuthorization()
        filtering = {
            'follower':('exact'),
            'followee':('exact'),
        }

    def dehydrate(self, bundle):
        # bundle.data['like_count'] = bundle.obj.likes.count() 
        if 'follower' in bundle.request.GET.keys():
            bundle.data.pop('follower')
        if 'followee' in bundle.request.GET.keys():
            bundle.data.pop('followee')
        # bundle.data.pop('favourites')
        return bundle