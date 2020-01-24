from haystack.forms import FacetedSearchForm
from django.contrib.postgres import forms as pg_forms


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
