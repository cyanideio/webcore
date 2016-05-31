#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication
from kada.models import SceneSet
from kada.api.scene_template import SceneTemplateResource
from tastypie import fields

class SceneSetResource(BaseResource):
    scenes = fields.ToManyField(SceneTemplateResource, 'scene_set', null=True, full=True)
    class Meta:
        queryset = SceneSet.objects.all()
        authentication = BaseAuthentication()