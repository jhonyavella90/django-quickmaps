from __future__ import absolute_import

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .widgets import LatLngWidget, MapWidget


class LatLngField(forms.MultiValueField):
    """Subclass of ``MultiValueField`` that creates two
    ``FloatField``s for latitude and longitude respectively.
    """
    widget = LatLngWidget
    default_error_messages = {
        'invalid_latitude':  _(u'Enter a valid latitude.'),
        'invalid_longitude': _(u'Enter a valid longitude.')
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        fields = (
            forms.FloatField(
                label=_(u'Latitude'),
                error_messages={'invalid': errors['invalid_latitude']},
                localize=localize
            ),
            forms.FloatField(
                label=_(u'Longitude'),
                error_messages={'invalid': errors['invalid_longitude']},
                localize=localize
            ),
        )
        super(LatLngField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if not data_list:
            return {}
        if data_list[0] in validators.EMPTY_VALUES:
            raise ValidationError(self.error_messages['invalid_latitude'])
        if data_list[1] in validators.EMPTY_VALUES:
            raise ValidationError(self.error_messages['invalid_longitude'])
        return {
            'latitude':  data_list[0],
            'longitude': data_list[1],
        }


class MapField(LatLngField):
    """Subclass of ``LatLngField`` that uses a ``MapWidget`` to render
    and adds an extra field for clearing the location.
    """
    widget = MapWidget

    def __init__(self, *args, **kwargs):
        """Adds an extra `clear_location` field."""
        super(MapField, self).__init__(*args, **kwargs)
        localize = kwargs.get('localize', False)
        self.fields += (
            forms.BooleanField(initial=False, required=False,
                               localize=localize),
        )

    def compress(self, data_list):
        if data_list and data_list[2]:
            return {}
        return super(MapField, self).compress(data_list)
