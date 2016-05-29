#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication
from core.models import Comment

class CommentResource(BaseResource):
    class Meta:
        queryset = Comment.objects.all()
        authentication = BaseAuthentication()