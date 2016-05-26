#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseKadaAuthentication
from core.models import Comment

class CommentResource(KadaResource):
    class Meta:
        queryset = Comment.objects.all()
        authentication = BaseKadaAuthentication()