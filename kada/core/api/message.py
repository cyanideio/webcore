#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import Message

class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()