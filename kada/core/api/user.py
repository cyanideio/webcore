#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from kada.utils.resource import KadaResource, ErrorFormatedModelResource
from core.models import UserProfile
from tastypie import fields
from tastypie.models import ApiKey
from tastypie.authentication import Authentication,ApiKeyAuthentication
from tastypie.authorization import Authorization,DjangoAuthorization

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

class UserProfileResource(KadaResource):
    """用户信息
    """
    user = fields.ToOneField('core.api.user.UserResource', attribute='user', related_name='user_profile')
    class Meta:
        excludes = ['user','oauth_token','mobile']
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

class UserLoginProfileResource(KadaResource):
    """用户信息
    """
    user = fields.ToOneField('core.api.user.LoginResource', attribute='user', related_name='user_profile')
    class Meta:
        excludes = ['user','oauth_token','mobile','id']
        queryset = UserProfile.objects.all()
        resource_name = 'user_login_profile'

class UserResource(KadaResource):
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

def is_login(request):
    """Custom Verification Methods
    """
    if 'username' in request.GET and ('password' in request.GET or 'oauth_token' in request.GET):
        return True
    else:
        return False

def get_real_username(username, mobile_num, user_from='self'):
    if user_from == 'self':
        assert mobile_num
        return mobile_num
    else:
        assert username
        return '%s%s' % (FROM_PREFIX.get(user_from), username)

def kada_auth(username, password=None, oauth_token=None, login=False):
    user = None
    # 两种密文中同时只能使用一种
    if sum(map(lambda x: 1 if x else 0, [password, oauth_token])) != 1:
        # TODO logging
        return user

    if password:
        user = authenticate(username=username,password=password)
    elif oauth_token:
        user = oauth_token_auth(username=username,token=oauth_token)
    if user is not None and login:
        refresh_apikey(user)
        user._last_login = user.last_login
        user.last_login = datetime.datetime.now()
        user.save()

    return user

def refresh_apikey(user):
    key = ApiKey.objects.get(user=user)
    key.key = key.generate_key()
    key.save()

class LoginResource(ErrorFormatedModelResource):
    """Login Resource For Users 
    """
    user_profile = fields.ToOneField(UserLoginProfileResource, 'user_profile', related_name='user', full=True)
    class Meta:
        filtering = {
            'username':('exact')
        } 
        queryset = User.objects.filter(is_superuser=False).all()
        allowed_methods = ['get']

        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser','is_staff']
        # authentication = Authentication()
        # authorization = DjangoAuthorization()

    # def get_object_list(self, request):
    #     if is_login(request):
    #         return super(LoginResource, self).get_object_list(request)
    #     return User.objects.none()

    # def build_filters(self, filters):
    #     if filters.get('from', 'self') != 'self':
    #         filters['username'] = get_real_username(filters['username'], filters['username'], filters['from'])
    #     return super(LoginResource, self).build_filters(filters)

    def dehydrate(self,bundle):
        username = bundle.request.GET['username']
        real_username = username
        # real_username = get_real_username(username, username, bundle.request.GET.get('from', 'self'))
        password = bundle.request.GET.get('password')
        oauth_token = bundle.request.GET.get('oauth_token')
        # 两种密文中同时只能使用一种
        if sum(map(lambda x: 1 if x else 0, [password, oauth_token])) != 1:
            bundle.data = {'is_authenticated':0,'msg':CREDENTIAL_INCORRECT}

        user = kada_auth(username=real_username, password=password, oauth_token=oauth_token, login=True)
        if user is not None:
            if user.is_active:
                key = ApiKey.objects.get(user=user).key
                bundle.data['is_authenticated'] = 1
                bundle.data['msg'] = USER_AUTHENTICATED
                bundle.data['key']= key
                bundle.data['last_login'] = user._last_login

                # 检查最近的系统消息，如果没有接收过的则创建接收关系
                # messages = system_message()
                # received = To.objects.filter(receiver=user).filter(
                #         entity__in=messages).all()
                # for m in (x for x in messages if x not in (y.entity for y in received)):
                #     To.objects.create(receiver=user, entity=m)
            else:
                bundle.data = {'is_authenticated':0,'msg':USER_DISABLED}
        else:
            bundle.data = {'is_authenticated':0,'msg':USRNAME_PWD_INCORRECT}
        return bundle