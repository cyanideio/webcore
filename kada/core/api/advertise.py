#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from core.models import Advertise

class AdvertiseResource(KadaResource):
    class Meta:
        queryset = Advertise.objects.all()