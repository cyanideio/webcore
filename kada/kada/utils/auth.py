#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.models import ApiKey
from django.db.models import Q
from tastypie.exceptions import Unauthorized

class BaseKadaAuthentication(ApiKeyAuthentication):
    """docstring for BaseKadaAuthentication"""
    def __init__(self):
        super(BaseKadaAuthentication, self).__init__()         

class FriendsAuthorization(Authorization):

    def __init__(self, arg):
        self.DIRECTION = {'fans':'followee', 'follows':'follower'}
        if arg not in self.DIRECTION.keys():
            raise Unauthorized("Sorry, Unauthorized")
        self.resource_type = self.DIRECTION[arg]
        super(FriendsAuthorization, self).__init__()         

    def read_list(self, object_list, bundle):
        print bundle.request
        if not bundle.request.GET.has_key(self.resource_type):
            raise Unauthorized("Sorry, Unauthorized")
        return object_list

    def read_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.creator.pk == bundle.request.user.pk

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

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

class MessageAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        user = bundle.request.user
        return object_list.filter(Q(author=user)|Q(target=user.id)).all()

    def read_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.creator.pk == bundle.request.user.pk

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.") 