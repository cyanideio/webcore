#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import Advertise

class AdvertiseResource(ModelResource):
    class Meta:
        queryset = Advertise.objects.all()