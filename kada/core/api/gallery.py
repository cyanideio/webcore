#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import Count
from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from kada.utils.auth import BaseKadaAuthentication
from kada.utils.resource import KadaResource
from kada.utils.custom_fields import CommaSeparatedIntegerField
from core.api.user import UserResource
from core.models import Gallery, Photo, Scene, SceneTemplate

LIKES_LIMIT = 6

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
    favourites = fields.ToManyField(UserResource, 'favourites', null=True, full=True)
    likes = fields.ToManyField(UserResource, 'likes', null=True, full=True)
    like_count = fields.IntegerField(readonly=True)

    class Meta:
        authentication = BaseKadaAuthentication()
        queryset = Gallery.objects.all()
        ordering = ['likes']
        filtering = {
            'created': ALL,
            'favourites': ('exact'),
            'author': ALL_WITH_RELATIONS,
            'type_kbn': ('exact')
        }

    def get_object_list(self, request):
        return super(GalleryResource, self).get_object_list(request).annotate(like_count=Count('likes', distinct=True))

    def dehydrate_like_count(self, bundle):
        return bundle.obj.like_count

    def dehydrate(self, bundle):
        # bundle.data['like_count'] = bundle.obj.likes.count() 
        bundle.data.pop('favourites')
        bundle.data['favourited'] = bundle.obj.favourites.filter(id=bundle.request.user.id).count()
        bundle.data['liked'] = bundle.obj.likes.filter(id=bundle.request.user.id).count()
        bundle.data['likes'] = bundle.data['likes'][0:LIKES_LIMIT]
        return bundle