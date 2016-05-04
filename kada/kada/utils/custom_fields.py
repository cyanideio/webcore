from tastypie.fields import CharField
from tastypie.exceptions import ApiFieldError

class CommaSeparatedIntegerField(CharField):
    """
    Converts django's string field to and from a list
    """

    def dehydrate(self, bundle, for_list=True):
        value = getattr(bundle.obj, self.attribute, None)
        if value is not None:
            try:
                return [int(pk) for pk in value.split(',')]
            except ValueError:
                # If a value can't be converted to int the field will
                # return null
                return None

    def hydrate(self, bundle):
        if self.instance_name not in bundle.data:
            return None

        value = bundle.data[self.instance_name]

        if value is None or len(value) == 0:
            return None

        value = str(value).lstrip('[').rstrip(']')
        try:
            [int(pk) for pk in value.split(',')]
            return value
        except ValueError:
            raise ApiFieldError('The field %s must be an int array or null'
                                % (self.instance_name))