#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import datetime
from tastypie.models import ApiKey
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
from core.models import UserProfile
from core.auth.utils import get_real_username
from django.core.exceptions import ObjectDoesNotExist

# Return Message for login
R = {
    'is_authenticated': 0,
    'msg': '',
}

# Return Message for register
R_REG = {
    'register_succeed': 0,
    'msg': '',
}


# Return Message for register
R_VER = {
    'v_code_sent': 0,
    'msg': '',
}

USER_EXISTS = _('That User Already Exists')
USER_AUTHENTICATED = _('User Authenticated')
USRNAME_PWD_INCORRECT = _('Username or Password Incorrect')
CREDENTIAL_INCORRECT = _('Credential Incorrect')
USER_DISABLED = _('User Disabled')

def user_auth(username, password=None, oauth_token=None, login=False):
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

# Login API
@csrf_exempt
def login(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    oauth_token = request.POST.get("oauth_token", "")
    real_username = username

    if sum(map(lambda x: 1 if x else 0, [password, oauth_token])) != 1:
        R['is_authenticated'] = 0
        R['msg'] = unicode(CREDENTIAL_INCORRECT)

    user = user_auth(username=real_username, password=password, oauth_token=oauth_token, login=True)
    if user is not None:
        if user.is_active:
            profile = UserProfile.objects.get(user=user)
            key = ApiKey.objects.get(user=user).key
            R['is_authenticated'] = 1
            R['msg'] = unicode(USER_AUTHENTICATED)
            R['key']= key
            R['user_info'] = json.loads(serializers.serialize('json', [user]))[0]['fields']
            R['user_profile'] = json.loads(serializers.serialize('json', [profile]))[0]['fields']

            # 检查最近的系统消息，如果没有接收过的则创建接收关系
            # messages = system_message()
            # received = To.objects.filter(receiver=user).filter(
            #         entity__in=messages).all()
            # for m in (x for x in messages if x not in (y.entity for y in received)):
            #     To.objects.create(receiver=user, entity=m)

        else:
            R['is_authenticated'] = 0
            R['msg'] = unicode(USER_DISABLED)
    else:
        R['is_authenticated'] = 0
        R['msg'] = unicode(USRNAME_PWD_INCORRECT)

    return JsonResponse(R)

# Register API
@csrf_exempt
def register(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    if username + password != "":
        _user, user_created = User.objects.get_or_create(username=username)
        if not user_created:
            # User Exists Change Password
            R_REG['msg'] = unicode(USER_EXISTS)
        else:
            # User Does not Exist
            _user.set_password(password) 
    else:
        pass
        # Wrong
    return JsonResponse(R_REG)

# Verification Code API
@csrf_exempt
def verify(request):
    username = request.POST.get("username", "")
    real_username = get_real_username(username)
    try:
        _user = User.objects.get(username=real_username)
    except ObjectDoesNotExist:
        print _user
    # R_VER['msg'] = unicode(USER_EXISTS)
    # R_VER['v_code_sent'] = 1
    r = "This is a Dummy API %s " % real_username
    return HttpResponse(r)