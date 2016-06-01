#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication, WriteOnlyAuthorization
from kada.models import Photo
from django.contrib.auth.models import User

class PhotoResource(BaseResource):
    class Meta:
        queryset = Photo.objects.all()
        authentication = BaseAuthentication()
        authorization = WriteOnlyAuthorization()