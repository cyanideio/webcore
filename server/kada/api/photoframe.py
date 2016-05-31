#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication, ReadOnlyAuthorization
from kada.models import PhotoFrame

class PhotoFrameResource(BaseResource):
    class Meta:
        queryset = PhotoFrame.objects.all()
        authentication = BaseAuthentication()
        authorization = ReadOnlyAuthorization()