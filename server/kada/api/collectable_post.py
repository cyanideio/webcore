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

from kada.models import Gallery
from core.models import Message

USER_INVALID = _('That User Does Not Exist')
INSUFFICIENT_PARAM = _('Insufficient PARAMs')
SUCCESS = _('Success')

DATA_KEYS = [u'collectable', u'type', u'action', u'id']

COLLECTABLES = {
    'gallery': Gallery 
}

KEY_TYPES = ['like', 'favourite']

def key_auth(user, skey):
    key = ApiKey.objects.get(user=user).key
    return key == skey

# real_username = get_real_username(username)

# Collectable API
@csrf_exempt
def collectable_post(request):
    # Return Message for gallery_post
    R = {
        'created': 0,
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
                    collectable = set(data.keys()) == set(DATA_KEYS)
                    if collectable:
                        if save_collectable(data, _user):
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

def save_collectable(data, user):
    collectable = data['collectable']
    key_type = data['type']
    id = data['id']
    action = data['action']
    if collectable in COLLECTABLES.keys() and key_type in KEY_TYPES:
        model = COLLECTABLES[collectable]
        try:
            obj = model.objects.get(id=id)
        except ObjectDoesNotExist:
            return False
        if key_type == 'like':
            if action == 'add':
                obj.likes.add(user)
                exp = datetime.datetime.now() + datetime.timedelta(days=365)
                Message.objects.create(author=user, target=obj.author, jump_target=obj.id, title="你的作品被点赞了！", msg_type=1, content="你的作品被点赞了！", system=False, expires=exp)
            elif action == 'remove':
                return False
            else:
                return False
        if key_type == 'favourite':
            if action == 'add':
                obj.favourites.add(user)
            elif action == 'remove':
                obj.favourites.remove(user)
            else:
                return False
        obj.save()
        return True