#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication, ReadOnlyAuthorization
from kada.models import SceneTemplate
from kada.api.photoframe import PhotoFrameResource
from tastypie import fields

class SceneTemplateResource(BaseResource):
    frames = fields.ToManyField(PhotoFrameResource, 'scene_template', null=True, full=True)
    class Meta:
        queryset = SceneTemplate.objects.all()
        authentication = BaseAuthentication()
        authorization = ReadOnlyAuthorization()