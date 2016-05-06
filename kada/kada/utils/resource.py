#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from tastypie import resources
from tastypie import http

def build_content_type(format, encoding='utf-8'):
    """
    Appends character encoding to the provided format if not already present.
    """
    if 'charset' in format:
        return format

    return "%s; charset=%s" % (format, encoding)

class KadaResource(resources.ModelResource):
    def create_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        Extracts the common "which-format/serialize/return-response" cycle.

        Mostly a useful shortcut/hook.
        """
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)
        return response_class(content=serialized, content_type=build_content_type(desired_format), **response_kwargs)

class ErrorFormatedModelResource(KadaResource):
    """

    将400的情况中返回的body统一为
    {"error" : [<e1>, ... ,<en>]}
    e1 ... en 分别是描述每个错误的字符串
    """

    def error_response(self, request, errors, response_class=None):
        if response_class is None or issubclass(response_class, http.HttpBadRequest):
            # in this case response_class will be decided in super.error_response
            # which now is BadRequest
            _errors = {"error":[]}
            if isinstance(errors, dict):
                # ApiFieldError & Validation errors 应该都是dict形式的
                for k, v in errors.iteritems():
                    if isinstance(v, (str, unicode)):
                        _errors['error'].append(v)
                    elif isinstance(v, dict):
                        _errors['error'].extend(v.values())
                    else:
                        # TODO log?
                        pass
            else:
                # TODO log?
                _errors['error'].append(str(errors))
        else:
            _errors = errors

        return super(ErrorFormatedModelResource, self).error_response(request, _errors, response_class=response_class)