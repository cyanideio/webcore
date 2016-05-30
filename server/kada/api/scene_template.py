#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication
from kada.models import SceneTemplate

class SceneTemplateResource(BaseResource):
    class Meta:
        queryset = SceneTemplate.objects.all()
        authentication = BaseAuthentication()