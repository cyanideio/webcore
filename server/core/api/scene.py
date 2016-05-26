#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseKadaAuthentication, CreateDeleteAuthorization
from kada.utils.custom_fields import CommaSeparatedIntegerField
from core.models import Scene
from core.api.gallery import GalleryResource

class SceneResource(KadaResource):
    gallery = fields.ToOneField(GalleryResource, 'profile')
    photo_seq = CommaSeparatedIntegerField(attribute='photo_seq') 
    class Meta:
        queryset = Scene.objects.all()
        authentication = BaseKadaAuthentication()
        authorization = CreateDeleteAuthorization()