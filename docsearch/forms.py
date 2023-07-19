import json

from django.forms import ModelForm, ValidationError
from django.contrib.gis.forms.fields import GeometryCollectionField
from django.contrib.gis.geos.collections import GeometryCollection
from django.contrib.gis.gdal.error import GDALException
from haystack.query import SQ
from haystack.forms import SearchForm

from docsearch.models import License
from docsearch.query import FuzzyAutoQuery


class BaseSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        self.selected_facets = kwargs.pop("selected_facets", [])
        super().__init__(*args, **kwargs)

    def no_query_found(self):
        """If the user inputs no query, return all documents."""
        return self.searchqueryset.all()

    def search(self):
        sqs = super().search()

        if self.selected_facets:
            sqs = self._search_by_facets(sqs)

        return sqs

    def _search_by_facets(self, sqs: FuzzyAutoQuery) -> FuzzyAutoQuery:
        facet_filter = SQ()

        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            facet_filter |= SQ(**{field: sqs.query.clean(value)})

        sqs = sqs.filter(facet_filter)

        return sqs


class LicenseGeometryCollectionField(GeometryCollectionField):
    def to_python(self, value):
        """
        Convert the value to a GeometryCollection, not natively supported
        by GeoDjango.
        """
        if not value:
            return None
        
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

    # def clean_geometry(self):
    #     data = self.cleaned_data['geometry']
    #     # print('THE GEOMETRY IS:', data)
    #     # print('Valid:', data.valid)
    #     # print('Empty:', data.empty)
    #     # print('Coords:', data.num_coords)
    #     # print('Geom:', data.num_geom)
    #     # print(data.geojson)
    #     # print(dir(data))
    #     if not data.valid or data.empty:
    #         print("NOT VALID")
    #         raise ValidationError(("Please enter valid GeoJSON"))
        
    #     return data

    class Meta:
        model = License
        fields = '__all__'
