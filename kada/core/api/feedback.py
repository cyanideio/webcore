#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import Feedback

class FeedbackResource(ModelResource):
    class Meta:
        queryset = Feedback.objects.all()