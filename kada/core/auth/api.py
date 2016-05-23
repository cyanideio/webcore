#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Login View
@csrf_exempt
def login(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    r = "This is a Dummy API %s %s" % (username, password)
    return HttpResponse(r)