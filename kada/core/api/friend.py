#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseFriendsAuthentication
from core.api.user import UserResource
from core.models import Friend

def friend_verify_has_key(ori_class):
    def get_object_list(self, request):
        same = list(set(request.GET.keys()).intersection(set(self.verify_keys)))
        for key in self.verify_keys:
            if not key in same:
                return Friend.objects.none()
        return super(ori_class, self).get_object_list(request)

    ori_class.get_object_list = get_object_list
    return ori_class

@friend_verify_has_key
class FriendFollowerResource(KadaResource):
    verify_keys = ['follower']
    follower = fields.ToOneField(UserResource, 'follower', null=True, full=True)
    class Meta:
        resource_name = 'friend/follows'
        queryset = Friend.objects.all()
        authentication = BaseFriendsAuthentication('follows')
        filtering = {
            'follower':('exact'),
        }


@friend_verify_has_key
class FriendFolloweeResource(KadaResource):
    verify_keys = ['followee']
    followee = fields.ToOneField(UserResource, 'followee', null=True, full=True)
    class Meta:
        resource_name = 'friend/fans'
        queryset = Friend.objects.all()
        authentication = BaseFriendsAuthentication('fans')
        filtering = {
            'followee':('exact'),
        }