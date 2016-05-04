#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import Gallery

class GalleryResource(ModelResource):
    class Meta:
        queryset = Gallery.objects.all()