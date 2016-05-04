#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from kada.utils.custom_fields import CommaSeparatedIntegerField
from core.models import Scene

class SceneResource(KadaResource):
    photo_seq = CommaSeparatedIntegerField(attribute='photo_seq') 
    class Meta:
        queryset = Scene.objects.all()