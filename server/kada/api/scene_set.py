#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication
from kada.models import SceneSet

class SceneSetResource(BaseResource):
    class Meta:
        queryset = SceneSet.objects.all()
        authentication = BaseAuthentication()