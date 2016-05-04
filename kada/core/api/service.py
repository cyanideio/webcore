#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import Service

class ServiceResource(ModelResource):
    class Meta:
        queryset = Service.objects.all()