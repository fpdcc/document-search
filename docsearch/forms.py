import json

from django.forms import ModelForm
from django.contrib.gis.forms.fields import GeometryCollectionField
from haystack.forms import FacetedSearchForm

from docsearch.models import License


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
