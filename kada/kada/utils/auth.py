#!/usr/bin/python
# -*- coding: utf-8 -*-
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication,Authentication
from tastypie.models import ApiKey
from django.db.models import Q
from tastypie.exceptions import Unauthorized

class BaseKadaAuthentication(ApiKeyAuthentication):
    """docstring for BaseKadaAuthentication"""
    def __init__(self):
        super(BaseKadaAuthentication, self).__init__()         