#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
from django.contrib.auth.models import User
from django.db.models import Count
from tastypie.fields import ListField
from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from core.utils.auth import BaseAuthentication, DetailOnlyAuthorization, GalleryAuthorization
from tastypie.authentication import Authentication
from core.utils.resource import BaseResource
from core.utils.custom_fields import CommaSeparatedIntegerField
from core.api.user import UserResource
from core.models import Friend
from kada.models import Gallery, Photo, Scene, SceneTemplate, PhotoFrame

LIKES_LIMIT = 6

class PhotoFrameResource(BaseResource):
    """docstring for PhotoResource"""
    class Meta:
        queryset = PhotoFrame.objects.all()
        authentication = BaseAuthentication()

class SceneTemplateResource(BaseResource):
    """docstring for PhotoResource"""
    photo_frames = fields.ToManyField(PhotoFrameResource, 'scene_template', null=True, full=True)
    class Meta:
        queryset = SceneTemplate.objects.all()
        authentication = BaseAuthentication()

class PhotoResource(BaseResource):
    """docstring for PhotoResource"""
    class Meta:
        queryset = Photo.objects.all()
        authentication = BaseAuthentication()

class SceneResource(BaseResource):
    """docstring for SceneResource"""
    scene_template = fields.ToOneField(SceneTemplateResource, 'scene_template', related_name='scene_scene_template', full=True)
    class Meta:
        queryset = Scene.objects.all()
        authentication = BaseAuthentication()

class GalleryResource(BaseResource):
    """影集"""
    author = fields.ToOneField(UserResource, 'author', null=True, full=True)
    scene_seq = CommaSeparatedIntegerField(attribute='scene_seq')
    photos = fields.ToManyField(PhotoResource, 'photo_gallery', null=True, full=True)
    scenes = fields.ToManyField(SceneResource, 'scene_gallery', null=True, full=True)
    favourites = fields.ToManyField(UserResource, 'favourites', null=True, full=True)
    likes = fields.ToManyField(UserResource, 'likes', null=True, full=True)
    comments = fields.ToManyField('kada.api.comment.CommentResource', 'comment_gallery', null=True, full=True)
    like_count = fields.IntegerField(readonly=True)
    comment_count = fields.IntegerField(readonly=True)
    tags = ListField()

    class Meta:
        authentication = BaseAuthentication()
        authorization = GalleryAuthorization()
        queryset = Gallery.objects.all()
        ordering = ['likes', 'created']
        filtering = {
            'name': ('exact'),
            'created': ALL,
            'favourites': ('exact'),
            'author': ALL_WITH_RELATIONS,
            'type_kbn': ('exact')
        }

    def dehydrate_tags(self, bundle):
        return map(str, bundle.obj.tags.all())

    def build_filters(self, filters=None, ignore_bad_filters=True):
        if filters is None:
            filters = {}

        orm_filters = super(GalleryResource, self).build_filters(filters)

        if 'follower' in filters:
            try:
                f = User.objects.get(id=filters['follower'])
            except Exception:
                return orm_filters 

            following_ids = [friend.followee.id for friend in Friend.objects.filter(follower=f).all()]
            orm_filters['author__id__in'] = following_ids

        if 'tag' in filters:
            orm_filters['tags__name__in'] = filters['tag'].split(',')

        return orm_filters

    def get_object_list(self, request):
        return super(GalleryResource, self).get_object_list(request).annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comment_gallery', distinct=True),
        )

    def dehydrate_like_count(self, bundle):
        return bundle.obj.like_count

    def dehydrate_comment_count(self, bundle):
        return bundle.obj.comment_count

    def dehydrate(self, bundle):
        # bundle.data['like_count'] = bundle.obj.likes.count() 
        bundle.data.pop('favourites')
        bundle.data.pop('comments')
        bundle.data['favourited'] = bundle.obj.favourites.filter(id=bundle.request.user.id).count()
        bundle.data['liked'] = bundle.obj.likes.filter(id=bundle.request.user.id).count()
        bundle.data['likes'] = bundle.data['likes'][0:LIKES_LIMIT]
        return bundle

class GalleryShareResource(GalleryResource):
    class Meta:
        list_allowed_methods = []
        detail_allowed_methods = ['get']
        authorization = DetailOnlyAuthorization()
        authentication = Authentication()
        queryset = Gallery.objects.all()

    def obj_get(self, bundle, **kwargs):
        try:
            pk = base64.b64decode(kwargs['pk'])[4:-4]
        except Exception:
            raise self._meta.object_class.DoesNotExist("Couldn't find an instance")
        kwargs['pk'] = pk
        return super(GalleryShareResource, self).obj_get(bundle, **kwargs)