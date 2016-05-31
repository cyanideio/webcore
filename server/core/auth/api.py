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
from core.auth.utils import get_real_username, send_vcode, vcode_varified
from django.core.exceptions import ObjectDoesNotExist


VER_PURPOSE_LIST = ['register', 'retrieve']

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
USER_INVALID = _('That User Does Not Exist')
INVALID_PURPOSE = _('Invalid Purpose')
INVALID_PARAM = _('Invalid Parameter')
USER_AUTHENTICATED = _('User Authenticated')
USRNAME_PWD_INCORRECT = _('Username or Password Incorrect')
CREDENTIAL_INCORRECT = _('Credential Incorrect')
USER_DISABLED = _('User Disabled')
SUCCEED = _('Succeed')

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
    real_username = get_real_username(username)

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
            R['profile_id'] = profile.id
            R['user_id'] = user.id

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
    vcode = request.POST.get("vcode", "")

    if username + password + vcode != "":
        if vcode_varified(username, vcode):
            _user, user_created = User.objects.get_or_create(username=get_real_username(username))
            _user.set_password(password) 
            R_REG['msg'] = unicode(SUCCEED)
            R_REG['register_succeed'] = 1
            if user_created:
                key = ApiKey.objects.get(user=_user).key
                profile = UserProfile.objects.get(user=_user)
                profile.mobile = username
                profile.save()
                R_REG['key']= key
                R_REG['user_info'] = json.loads(serializers.serialize('json', [_user]))[0]['fields']
                R_REG['user_profile'] = json.loads(serializers.serialize('json', [profile]))[0]['fields']
                R_REG['profile_id'] = profile.id
                R_REG['user_id'] = user.id
    else:
        R_REG['msg'] = unicode(INVALID_PARAM)
        R_REG['register_succeed'] = 0
        # Wrong
    return JsonResponse(R_REG)

# Verification Code API
@csrf_exempt
def verify(request):
    username = request.POST.get("username", "")
    purpose = request.POST.get("purpose", "")  
    real_username = get_real_username(username)
    if purpose in VER_PURPOSE_LIST and username != '':
        try:
            _user = User.objects.get(username=real_username)
            if purpose == 'register':
                R_VER['msg'] = unicode(USER_EXISTS)
                R_VER['v_code_sent'] = 0
            else:
                R_VER['msg'], R_VER['v_code_sent'] = send_vcode(real_username, username)
        except ObjectDoesNotExist:
            if purpose == 'retrieve':
                R_VER['msg'] = unicode(USER_INVALID)
                R_VER['v_code_sent'] = 0
            else:
                R_VER['msg'], R_VER['v_code_sent'] = send_vcode(real_username, username)
    else:
        R_VER['msg'] = unicode(INVALID_PURPOSE)
        R_VER['v_code_sent'] = 0
    return JsonResponse(R_VER)