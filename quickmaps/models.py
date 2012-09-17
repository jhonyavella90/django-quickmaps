# Not really a models.py file, more of a models/fields.py

from __future__ import absolute_import

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from picklefield.fields import PickledObjectField

from .fields import MapField
from .utils import LatLngDict

def validate_lat_lng(value):
    """`value` must be a python dictionary and must have only two
    keys: 'latitude' and 'longitude'. The values for those keys must
    be either strings or floats.
    """
    if type(value) is not dict:
        raise ValidationError(_(u'%s is not a python dictionary.') % value)
    if not value.has_key('latitude'):
        raise ValidationError(_(u'%s should have a latitude key.') % value)
    if not value.has_key('longitude'):
        raise ValidationError(_(u'%s should have a longitude key.') % value)
    if len(value.keys()) != 2:
        raise ValidationError(_(u'%s should only have two keys.') % value)
    if type(value['latitude']) not in (str, float):
        raise ValidationError(
            _(u'latitude key in %s is not a string or a float') % value
        )
    if type(value['longitude']) not in (str, float):
        raise ValidationError(
            _(u'longitude key in %s is not a string or a float') % value
        )


class LatLngField(PickledObjectField):
    """Subclass of ``PickledObjectField`` that validates the object
    being saved is a python dictionary with only two keys: 'latitude'
    and 'longitude'. The values for these keys must be either floats,
    decimals of strings.
    """
    __metaclass__ = models.SubfieldBase

    _value = None

    default_validators = PickledObjectField.default_validators + \
                         [validate_lat_lng]

    def __init__(self, *args, **kwargs):
        """Subclass of ``PickledObjectField`` that makes this field
        editable.
        """
        super(LatLngField, self).__init__(*args, **kwargs)
        self.editable = True

    def get_db_prep_value(self, value, *args, **kwargs):
        """If the value is None, we convert it to an empty
        dictionary.
        """
        if not value:
            value = LatLngDict()
        elif not isinstance(value, LatLngDict):
            ll = LatLngDict()
            ll['latitude']  = value['latitude']
            ll['longitude'] = value['longitude']
            value = ll
        return super(LatLngField, self).get_db_prep_value(
            value, *args, **kwargs
        )

    def formfield(self, **kwargs):
        """Makes ``.fields.LatLngField`` the default field class."""
        form_class = kwargs.pop('form_class', MapField)
        return super(LatLngField, self).formfield(
            form_class=form_class, **kwargs
        )

# South support; see
# http://south.aeracode.org/docs/tutorial/part4.html#simple-inheritance
try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules(
        [], [r'^quickmaps\.models\.LatLngField']
    )
