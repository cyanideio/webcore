#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from kada.utils.resource import KadaResource
from kada.utils.auth import BaseKadaAuthentication, FeedbackAuthorization
from core.models import Feedback

class FeedbackResource(KadaResource):
    class Meta:
        queryset = Feedback.objects.all()
        authentication = BaseKadaAuthentication()
        authorization = FeedbackAuthorization()

    def hydrate(self, bundle, request=None):
        bundle.obj.author = User.objects.get(pk = bundle.request.user.id)
        return bundle 