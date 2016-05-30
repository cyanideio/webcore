#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.models import ApiKey
from django.db.models import Q
from tastypie.exceptions import Unauthorized

class BaseAuthentication(ApiKeyAuthentication):
    """docstring for BaseAuthentication"""
    def __init__(self):
        super(BaseAuthentication, self).__init__()         

class FriendsAuthorization(Authorization):

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

class CreateDeleteAuthorization(Authorization):

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
        return bundle

class MessageAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        user = bundle.request.user
        return object_list.filter(Q(author=user)|Q(target=user.id)|Q(system=True)).all()

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