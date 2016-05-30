#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication, CreateDeleteAuthorization
from core.utils.custom_fields import CommaSeparatedIntegerField
from kada.models import Scene
from kada.api.gallery import GalleryResource

class SceneResource(BaseResource):
    gallery = fields.ToOneField(GalleryResource, 'profile')
    photo_seq = CommaSeparatedIntegerField(attribute='photo_seq') 
    class Meta:
        queryset = Scene.objects.all()
        authentication = BaseAuthentication()
        authorization = CreateDeleteAuthorization()