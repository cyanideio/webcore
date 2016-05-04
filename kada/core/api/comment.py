#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from core.models import Comment

class CommentResource(KadaResource):
    class Meta:
        queryset = Comment.objects.all()