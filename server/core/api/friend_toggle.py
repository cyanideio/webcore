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
from django.core.exceptions import ObjectDoesNotExist

from core.models import Friend

USER_INVALID = _('That User Does Not Exist')
INSUFFICIENT_PARAM = _('Insufficient PARAMs')
SUCCESS = _('Success')

DATA_KEYS = [u'friend']

def key_auth(user, skey):
    key = ApiKey.objects.get(user=user).key
    return key == skey

# real_username = get_real_username(username)

# Collectable API
@csrf_exempt
def friend_toggle(request):
    # Return Message for gallery_post
    R = {
        'toggled': 0,
        'msg': '',
    }
    METHOD = request.META['REQUEST_METHOD']
    if 'HTTP_AUTHORIZATION' in request.META.keys() and METHOD == 'POST':
        AUTHINFO = request.META['HTTP_AUTHORIZATION']
        if len(AUTHINFO.split(':')) == 2:
            key = AUTHINFO.split(':')[1]
            if len(AUTHINFO.split(':')[0].split(' ')) == 2 and AUTHINFO.split(':')[0].split(' ')[0] == 'ApiKey':
                real_username = AUTHINFO.split(':')[0].split(' ')[1]
                # Auth Starts 
                try:
                    _user = User.objects.get(username=real_username)
                except ObjectDoesNotExist: 
                    R['msg'] = unicode(USER_INVALID)
                    return JsonResponse(R)
                if key_auth(_user, key):
                    data = json.loads(request.body) 
                    key_valid = set(data.keys()) == set(DATA_KEYS)
                    if key_valid:
                        if process_data(data, _user):
                            R['msg'] = unicode(SUCCESS)
                            R['created'] = 1 
                        else:
                            R['msg'] = unicode(INSUFFICIENT_PARAM)  
                    else:
                        R['msg'] = unicode(INSUFFICIENT_PARAM)  
                        
                else:
                    R['msg'] = unicode(USER_INVALID)
    else:
        R['created'] = 0
    return JsonResponse(R)

def process_data(data, user):
    id = data['friend']
    try:
        friend = User.objects.get(id=id)
    except ObjectDoesNotExist:
        return False
    try:
        friendship = Friend.objects.filter(follower__id=user.id).filter(followee__id=id).get()
        friendship.delete()
    except ObjectDoesNotExist:
        Friend.objects.create(followee=friend, follower=user)
    return True