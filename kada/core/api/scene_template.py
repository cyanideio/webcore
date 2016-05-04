#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import SceneTemplate

class SceneTemplateResource(ModelResource):
    class Meta:
        queryset = SceneTemplate.objects.all()