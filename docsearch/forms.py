import json

from django.forms import ModelForm
from django.contrib.gis.forms.fields import GeometryCollectionField
from haystack.forms import FacetedSearchForm
from django.contrib.postgres import forms as pg_forms

from docsearch.models import License


class InclusiveIntegerRangeField(pg_forms.IntegerRangeField):
    """
    Adjust the built-in Postgres range field so that its upper bound is
    inclusive instead of exclusive. See:
    https://code.djangoproject.com/ticket/27147#comment:5
    """
    _unit_value = 1

    def compress(self, values):
        range_value = super().compress(values)
        if range_value:
            return self.range_type(range_value.lower, range_value.upper, bounds='[]')

    def prepare_value(self, value):
        value = super().prepare_value(value)
        # We need to clean both fields
        value = [field.clean(val) for field, val in zip(self.fields, value)]
        if value[1] is not None:
            value[1] = value[1] - self._unit_value
        return value


class BaseSearchForm(FacetedSearchForm):
    def no_query_found(self):
        """If the user inputs no query, return all documents."""
        return self.searchqueryset.all()


class LicenseGeometryCollectionField(GeometryCollectionField):
    def to_python(self, value):
        """
        Convert the value to a GeometryCollection, not natively supported
        by GeoDjango.
        """
        val = json.loads(value)
        if val.get('type') != 'GeometryCollection':
            val = {
                'type': 'GeometryCollection',
                'geometries': [val]
            }
        return super().to_python(json.dumps(val))


class LicenseForm(ModelForm):
    geometry = LicenseGeometryCollectionField(help_text=(
        'All geometries are converted to GeometryCollections before being '
        'stored in the database. However, the map widget currently does not '
        'support drawing more than one feature on the map, so if you require '
        'multiple features for this geometry, define a custom GeoJSON '
        'GeometryCollection and paste it in the box above.'
    ))

    class Meta:
        model = License
        fields = '__all__'
