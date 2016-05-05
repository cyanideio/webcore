#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from kada.utils.resource import KadaResource
from kada.utils.custom_fields import CommaSeparatedIntegerField
from core.models import Gallery, Photo, Scene
from core.api.user import UserResource

class PhotoResource(KadaResource):
    """docstring for PhotoResource"""
    class Meta:
        queryset = Photo.objects.all()

class SceneResource(KadaResource):
    """docstring for SceneResource"""
    class Meta:
        queryset = Scene.objects.all()

class GalleryResource(KadaResource):
    """影集"""
    author = fields.ToOneField(UserResource, 'author', null=True, full=True)
    scene_seq = CommaSeparatedIntegerField(attribute='scene_seq')
    photos = fields.ToManyField(PhotoResource, 'photos', null=True, full=True)
    scenes = fields.ToManyField(SceneResource, 'scenes', null=True, full=True)
    class Meta:
        queryset = Gallery.objects.all()