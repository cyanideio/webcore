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

class DetailOnlyAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no lookups.")

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.follower.pk == bundle.request.user.pk

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

class FriendsAuthorization(Authorization):

    def read_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.follower.pk == bundle.request.user.pk

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        return bundle.obj.follower.pk == bundle.request.user.pk


class CreateDeleteAuthorization(Authorization):

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
        return True

class GalleryAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.author.pk == bundle.request.user.pk

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        # try:
        #     key, value = bundle.request.get_raw_uri().split('?')[1].split('=')
        # except Exception:
        #     raise Unauthorized("Sorry, no updates.")
        # if key == 'id':
        #     id = value
        #     print id
        #     return object_list
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        return True
        # raise Unauthorized("Sorry, no deletes.")

class MessageAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        user = bundle.request.user
        return object_list.filter(Q(author=user)|Q(target=user.id)|Q(system=True)).all()

    def read_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.") 

class ProfileAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list

    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def update_detail(self, object_list, bundle):
        if bundle.obj.user:
            return bundle.obj.user.pk == bundle.request.user.pk
        else:
            return False

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.") 

class ReadOnlyAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list.filter(Q(is_superuser=False)|Q(is_staff=False)).all()

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, UnAuthorized")

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, UnAuthorized")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.") 


class WriteOnlyAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        raise Unauthorized("Sorry, UnAuthorized")

    def read_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, UnAuthorized")

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

class UserAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no details")

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no updates.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.") 
