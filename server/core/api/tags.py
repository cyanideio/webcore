from taggit.models import Tag
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ALL_WITH_RELATIONS, ALL

class TagResource(BaseResource):
    class Meta:
        authentication = BaseAuthentication()
        authorization = ReadOnlyAuthorization()
        queryset = Tag.objects.all()

        filtering = {
            'name': ('exact'),
        }