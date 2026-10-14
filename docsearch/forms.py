import json

from django.forms import ModelForm, ValidationError, NumberInput, BaseInlineFormSet, inlineformset_factory
from django.contrib.gis.forms.fields import GeometryCollectionField
from haystack.query import SQ
from haystack.forms import SearchForm
from haystack.inputs import Exact

from docsearch.models import License, FlatDrawing, Coordinate
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

            if "_exact" in field:
                facet_filter |= SQ(**{field: Exact(value)})
            else:
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
        
        try:
            val = json.loads(value)
        except json.decoder.JSONDecodeError:
            raise ValidationError(("Please check the formatting for your GeoJSON"))

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

    def clean_geometry(self):
        data = self.cleaned_data['geometry']
        if not data.valid or data.empty:
            raise ValidationError(("Please enter valid GeoJSON"))
        
        return data

    class Meta:
        model = License
        fields = '__all__'


class CoordinateForm(ModelForm):
    class Meta:
        model = Coordinate
        fields = ['area', 'section']
        widgets = {
            'area': NumberInput(attrs={'class': 'form-control', 'max': 33}),
            'section': NumberInput(attrs={'class': 'form-control', 'max': 36}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set both fields as required
        # Blank "extra" rows skip validation, so this only affects rows users touch
        for field in self.fields.values():
            field.required = True
            field.widget.attrs['min'] = 1


class BaseCoordinateFormSet(BaseInlineFormSet):
    help_text = 'Both an area and section must be entered for each coordinate.'


CoordinateFormSet = inlineformset_factory(
    FlatDrawing,
    Coordinate,
    form=CoordinateForm,
    formset=BaseCoordinateFormSet,
    extra=0,             # Adding extra blank rows to be handled by js script
    min_num=1,           # A new drawing starts with one row,
    validate_min=True,   # and must keep at least one coordinate
    can_delete=True,
)
