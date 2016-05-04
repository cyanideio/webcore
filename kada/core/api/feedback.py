#!/usr/bin/python
# -*- coding: utf-8 -*-
from kada.utils.resource import KadaResource
from core.models import Feedback

class FeedbackResource(KadaResource):
    class Meta:
        queryset = Feedback.objects.all()