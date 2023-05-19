import json

from django.forms import ModelForm
from django.contrib.gis.forms.fields import GeometryCollectionField
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
