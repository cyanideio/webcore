#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from core.models import Service

class ServiceResource(KadaResource):
    class Meta:
        queryset = Service.objects.all()