#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import Comment

class CommentResource(ModelResource):
    class Meta:
        queryset = Comment.objects.all()