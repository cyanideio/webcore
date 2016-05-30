#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication, FeedbackAuthorization
from kada.models import Feedback

class FeedbackResource(BaseResource):
    class Meta:
        queryset = Feedback.objects.all()
        authentication = BaseAuthentication()
        authorization = FeedbackAuthorization()

    def hydrate(self, bundle, request=None):
        bundle.obj.author = User.objects.get(pk = bundle.request.user.id)
        return bundle 