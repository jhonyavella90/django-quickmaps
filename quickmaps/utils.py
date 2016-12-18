from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class LatLngDict(dict):
    """A two key'd dictionary for latitude and longitude values that
    knows how to display itself in various formats.
    """
    template_name = None

    def __str__(self):
        return self.as_comma_separated()

    def as_comma_separated(self):
        if not self:
            return ''
        return '%s, %s' % (self['longitude'], self['latitude'])

    def as_map(self, template_name=None, context=None):
        context = (context or {}).update(self)
        template_name = template_name or self.template_name
        if template_name is None:
            return ''
        return render_to_string(template_name or self.template_name, context)
