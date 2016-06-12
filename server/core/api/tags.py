from taggit.models import Tag
from core.utils.resource import BaseResource
from core.utils.auth import BaseAuthentication, ReadOnlyAuthorization

class TagResource(BaseResource):
    class Meta:
        authentication = BaseAuthentication()
        authorization = ReadOnlyAuthorization()
        queryset = Tag.objects.all()