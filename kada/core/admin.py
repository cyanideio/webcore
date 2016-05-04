from django.contrib import admin
# Register your models here.
from core.models import Friend, Gallery, Comment, Photo, SceneTemplate, Scene, ServiceType, Service, Advertise, Tip, Message, Feedback

class CommonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Friend, CommonAdmin)
admin.site.register(Gallery, CommonAdmin)
admin.site.register(Comment, CommonAdmin)
admin.site.register(Photo, CommonAdmin)
admin.site.register(SceneTemplate, CommonAdmin)
admin.site.register(Scene, CommonAdmin)
admin.site.register(ServiceType, CommonAdmin)
admin.site.register(Service, CommonAdmin)
admin.site.register(Advertise, CommonAdmin)
admin.site.register(Tip, CommonAdmin)
admin.site.register(Message, CommonAdmin)
admin.site.register(Feedback, CommonAdmin)