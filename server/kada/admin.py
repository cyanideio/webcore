#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dependencies
from django.contrib import admin
from core.admin import CommonAdmin

# Register your models here.
from kada.models import Gallery, Comment, Photo, SceneTemplate, Scene, ServiceType, Service, Advertise, Tip, Feedback, SceneSet

admin.site.register(Gallery, CommonAdmin)
admin.site.register(Comment, CommonAdmin)
admin.site.register(Photo, CommonAdmin)
admin.site.register(SceneTemplate, CommonAdmin)
admin.site.register(Scene, CommonAdmin)
admin.site.register(ServiceType, CommonAdmin)
admin.site.register(Service, CommonAdmin)
admin.site.register(Advertise, CommonAdmin)
admin.site.register(Tip, CommonAdmin)
admin.site.register(Feedback, CommonAdmin)
admin.site.register(SceneSet, CommonAdmin)
