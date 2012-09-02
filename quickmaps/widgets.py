try:
    import floppyforms as forms
except ImportError:
    from django import forms

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class LatLngWidget(forms.MultiWidget):
    """A widget that splits a python dictionary list for latitude and
    longitude into two inputs type=text.
    """
    def __init__(self, *args, **kwargs):
        widgets = (forms.TextInput(), forms.TextInput())
        super(LatLngWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            return [value['latitude'], value['longitude']]
        return [None, None]


class MapWidget(forms.MultiWidget):
    """A Widget that splits a python dictionary with two keys
    (latitude and longitude) into two <input type=hidden /> and
    renders a map after them.
    """
    default_location = {'latitude': 10.49929, 'longitude': -66.900558}  # Caracas.
    map_template_name = 'maps/map_widget.html'
    map_width  = 300
    map_height = 300
    map_zoom = 12

    def __init__(self, attrs=None, map_template_name=None, map_attrs=None):
        widgets = (forms.HiddenInput(attrs=attrs),
                   forms.HiddenInput(attrs=attrs),
                   forms.CheckboxInput(attrs=attrs),)
        self.map_template_name = map_template_name or self.map_template_name
        self.map_attrs = {
            'width': self.map_width,
            'height': self.map_height,
            'zoom': self.map_zoom,
        }
        self.map_attrs.update(map_attrs or {})
        super(MapWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value['latitude'], value['longitude'], False]
        return [None, None, False]

    def get_context(self, name, value, attrs):
        self.map_attrs['id'] = attrs['id']
        self.map_attrs['name'] = '%s_map' % name
        # Decide center and whether or not we need to set a marker.
        if value:
            location = value
            pin_marker = True
        else:
            location = self.default_location
            pin_marker = False

        return {
            'location': location,
            'pin_marker': pin_marker,
            'map': self.map_attrs,
            'input': {
                'latitude': attrs['id'] + '_0',
                'longitude': attrs['id'] + '_1'
            }
        }

    def render(self, name, value, attrs=None):
        """Renders the map after the input widgets."""
        map_render = render_to_string(self.map_template_name,
                                      self.get_context(name, value, attrs))
        widgets = super(MapWidget, self).render(name, value, attrs)
        clear_help_text = _(u'Clear this location.<br />')
        return mark_safe(widgets + clear_help_text + map_render)


    class Media:
        js = ('http://maps.googleapis.com/maps/api/js?key=%s&sensor=false' % \
              settings.GOOGLE_MAPS_KEY,)
