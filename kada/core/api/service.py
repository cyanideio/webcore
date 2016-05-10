#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseKadaAuthentication
from core.models import Service

class ServiceResource(KadaResource):
    class Meta:
        queryset = Service.objects.all()
        authentication = BaseKadaAuthentication()