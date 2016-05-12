#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS
from kada.utils.auth import BaseKadaAuthentication
from kada.utils.resource import KadaResource
from kada.utils.custom_fields import CommaSeparatedIntegerField
from core.models import Gallery, Photo, Scene, SceneTemplate
from core.api.user import UserResource

class SceneTemplateResource(KadaResource):
    """docstring for PhotoResource"""
    class Meta:
        queryset = SceneTemplate.objects.all()
        authentication = BaseKadaAuthentication()

class PhotoResource(KadaResource):
    """docstring for PhotoResource"""
    class Meta:
        queryset = Photo.objects.all()
        authentication = BaseKadaAuthentication()

class SceneResource(KadaResource):
    """docstring for SceneResource"""
    scene_template = fields.ToOneField(SceneTemplateResource, 'scene_template', related_name='scene_scene_template', full=True)
    class Meta:
        queryset = Scene.objects.all()
        authentication = BaseKadaAuthentication()

class GalleryResource(KadaResource):
    """影集"""
    author = fields.ToOneField(UserResource, 'author', null=True, full=True)
    scene_seq = CommaSeparatedIntegerField(attribute='scene_seq')
    photos = fields.ToManyField(PhotoResource, 'photo_gallery', null=True, full=True)
    scenes = fields.ToManyField(SceneResource, 'scene_gallery', null=True, full=True)
    favourites = fields.ToManyField(UserResource, 'Gallerys_favourites', null=True, full=True)
    class Meta:
        authentication = BaseKadaAuthentication()
        queryset = Gallery.objects.all()
        filtering = {
            'author': ALL_WITH_RELATIONS,
            'type_kbn':('exact')
        } 