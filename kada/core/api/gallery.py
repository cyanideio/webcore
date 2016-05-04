#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from kada.utils.custom_fields import CommaSeparatedIntegerField
from core.models import Gallery

class GalleryResource(KadaResource):
    scene_seq = CommaSeparatedIntegerField(attribute='scene_seq')
    class Meta:
        queryset = Gallery.objects.all()