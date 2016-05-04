#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import Friend

class FriendResource(ModelResource):
    class Meta:
        queryset = Friend.objects.all()