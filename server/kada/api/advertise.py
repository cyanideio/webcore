#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.utils.resource import BaseResource
from kada.models import Advertise

class AdvertiseResource(BaseResource):
    class Meta:
        queryset = Advertise.objects.all()