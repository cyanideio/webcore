#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)
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

from kada.models import Photo, Scene, SceneTemplate, Gallery

USER_INVALID = _('That User Does Not Exist')
INSUFFICIENT_PARAM = _('Insufficient PARAMs')
SUCCESS = _('Success')
DATA_KEYS_ISHIYAKI = [u'name', u'tags', u'photos', u'type', u'description']
DATA_KEYS_KADA = [u'name', u'tags', u'photos', u'type', u'description', u'scene_seq', u'scenes']

def key_auth(user, skey):
    key = ApiKey.objects.get(user=user).key
    return key == skey

# real_username = get_real_username(username)

# Gallery Post API
@csrf_exempt
def gallery_post(request):
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
                    kada = data['type'] == 0 and set(data.keys()) == set(DATA_KEYS_KADA)
                    ishiyaki = data['type'] == 1 and set(data.keys()) == set(DATA_KEYS_ISHIYAKI)
                    if kada or ishiyaki:
                        if save_gallery(data, _user):
                            R['msg'] = unicode(SUCCESS)
                            R['created'] = 1 
                    else:
                        R['msg'] = unicode(INSUFFICIENT_PARAM)  
                else:
                    R['msg'] = unicode(USER_INVALID)
    else:
        R['created'] = 0
    return JsonResponse(R)

def save_gallery(data, user):
    name = data['name']
    description = data['description']
    type_kbn = data['type']
    tags = data['tags']
    photos = data['photos']
    scenes = data['scenes']
    scene_seq = data['scene_seq']
    photoEntries = {}
    g = Gallery.objects.create(
        author = user,
        name = name,
        description  = description,
        type_kbn = type_kbn
    )
    for photo in photos:
        index = photo['index']
        p = Photo(
            author = user,
            exif = photo['exif'],
            image = photo['image']
        )
        p.save()
        photoEntries[index] = p

    # For Ishiyaki Only   
    if type_kbn == 0:
        sceneEntries = {}
        print photoEntries
        for scene in scenes:
            index = scene['index']
            photoseq = []
            for photoIndex in scene['photo_seq']:
                photoseq.append(str(photoEntries[photoIndex].id))
            s = Scene.objects.create(
                scene_template = SceneTemplate.objects.get(id=int(scene['scene_template'])),
                photo_seq = ",".join(photoseq),
                gallery = g
            )
            sceneEntries[index] = s
        sceneseq = []
        for sceneIndex in scene_seq:
            sceneseq.append(str(sceneEntries[sceneIndex].id))
        g.scene_seq = ",".join(sceneseq)
        g.save()
    for tag in tags:
        g.tags.add(tag)
    g.save()
    for photo in photoEntries.values():
        photo.gallery.add(g)
        photo.save()
    return True
