#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from core.utils.resource import BaseResource, ErrorFormatedModelResource, TaggableResource
from core.utils.auth import BaseAuthentication, ProfileAuthorization, ReadOnlyAuthorization
from core.models import UserProfile

from tastypie import fields
from tastypie.models import ApiKey
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization

FROM_PREFIX = {
    'self' : '',
    'weixin' : 'weixin_',
}

USER_DISABLED = _('User Disabled')
USER_AUTHENTICATED = _('User Authenticated')
USRNAME_PWD_INCORRECT = _('Username or Password Incorrect')
CREDENTIAL_INCORRECT = _('Credential Incorrect')
USER_EXISTS = _('That User Already Exists')
MOBILE_EXISTS = _('That Number Already Exists')
INVALIDE_USER_TYPE = _('Invalid User Type')
INVALIDE_MOBILE = _('Invalid Mobile Number')
INSUFFICIENT_INFORMATION = _('Insufficient Information')
VERIFICATION_CODE_DOESNOT_EXIST = _('Verification Code Does Not Exist')
INVALID_USERNAME = _('Invalid Username')

class UserProfileResource(TaggableResource):
    """用户信息
    """
    user = fields.ToOneField('core.api.user.UserResource', attribute='user', related_name='user_profile')

    class Meta:
        excludes = ['user','oauth_token','mobile']
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'
        authentication = BaseAuthentication()
        authorization = ProfileAuthorization()
        filtering = {
            'nickname': ('exact'),
        }

    def hydrate(self, bundle):
        # Don't change existing slugs.
        # In reality, this would be better implemented at the ``Note.save``
        # level, but is for demonstration.
        if 'email' in bundle.data.keys():
            u = bundle.request.user
            u.email = bundle.data['email']
            u.save()
        return bundle

class UserResource(BaseResource):
    """用户
    """
    user_profile = fields.ToOneField(UserProfileResource, 'user_profile', related_name='user', full=True)
    class Meta:
        excludes = [
            'email', 'password', 
            'is_superuser','is_staff', 
            'last_login', 'first_name', 
            'last_name', 'is_active', 
            'date_joined', 'username'
        ]
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = BaseAuthentication()
        authorization = ReadOnlyAuthorization()