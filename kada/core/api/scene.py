#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import Scene

class SceneResource(ModelResource):
    class Meta:
        queryset = Scene.objects.all()