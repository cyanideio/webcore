#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseKadaAuthentication
from core.models import Message

class MessageResource(KadaResource):
    class Meta:
        queryset = Message.objects.all()
        authentication = BaseKadaAuthentication()