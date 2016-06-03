#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication
from tastypie.authorization import Authorization
from tastypie.fields import ForeignKey
from kada.models import Comment
from kada.api.gallery import GalleryResource

class CommentResource(BaseResource):
    gallery = ForeignKey(GalleryResource, 'gallery')

    class Meta:
        queryset = Comment.objects.all()
        authentication = BaseAuthentication()
        authorization = Authorization()
        filtering = {
            'gallery': ('exact')
        }


    def hydrate(self, bundle, request=None):
        bundle.obj.author = User.objects.get(pk = bundle.request.user.id)
        return bundle 