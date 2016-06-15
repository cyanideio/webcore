#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dependencies
from django.contrib import admin
from core.admin import CommonAdmin
from django.contrib.admin import TabularInline, StackedInline, site
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin


# Register your models here.
from kada.models import Gallery, Comment, Photo, SceneTemplate, Scene, ServiceType, Service, Advertise, Tip, Feedback, SceneSet, PhotoFrame

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
# admin.site.register(SceneSet, CommonAdmin)
admin.site.register(PhotoFrame, CommonAdmin)


class UserProfileInline(admin.TabularInline):
    model = SceneTemplate.scene_set.through

class UserProfileAdmin(CommonAdmin):
    inlines = [ UserProfileInline, ]

admin.site.register(SceneSet, UserProfileAdmin)


# class RoomInlineAdmin(SuperInlineModelAdmin, TabularInline):
#     model = Room


# class HouseInlineAdmin(SuperInlineModelAdmin, StackedInline):
#     model = SceneTemplate.scene_set.through
#     # inlines = (RoomInlineAdmin,)


# class OwnerAdmin(SuperModelAdmin):
#     inlines = (HouseInlineAdmin,)


# site.register(SceneTemplate, OwnerAdmin)