#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication
from tastypie.authorization import Authorization
from kada.models import Feedback

class FeedbackAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no lookups.")

    def read_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.author.pk == bundle.request.user.pk

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

class FeedbackResource(BaseResource):
    class Meta:
        queryset = Feedback.objects.all()
        authentication = BaseAuthentication()
        authorization = FeedbackAuthorization()

    def hydrate(self, bundle, request=None):
        bundle.obj.author = User.objects.get(pk = bundle.request.user.id)
        return bundle 