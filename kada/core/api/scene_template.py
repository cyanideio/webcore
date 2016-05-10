#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseKadaAuthentication
from core.models import SceneTemplate

class SceneTemplateResource(KadaResource):
    class Meta:
        queryset = SceneTemplate.objects.all()
        authentication = BaseKadaAuthentication()