#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from kada.utils.resource import KadaResource
from core.models import UserProfile
from tastypie import fields

class UserProfileResource(KadaResource):
    """用户信息
    """
    user = fields.ToOneField('core.api.user.UserResource', attribute='user', related_name='user_profile')
    class Meta:
        excludes = ['user','oauth_token','mobile']
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

class UserResource(KadaResource):
    """用户
    """
    user_profile = fields.ToOneField(UserProfileResource, 'user_profile', related_name='user', full=True)
    class Meta:
        excludes = ['email', 'password', 'is_superuser','is_staff', 'last_login', 'first_name', 'last_name', 'is_active', 'date_joined']
        queryset = User.objects.all()
        resource_name = 'user'