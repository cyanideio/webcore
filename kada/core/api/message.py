#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from core.models import Message

class MessageResource(KadaResource):
    class Meta:
        queryset = Message.objects.all()