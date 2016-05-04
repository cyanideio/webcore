#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from core.models import Friend

class FriendResource(KadaResource):
    class Meta:
        queryset = Friend.objects.all()