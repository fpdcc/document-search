from django import template
from django.utils.text import capfirst

from .model_meta import field_name

register = template.Library()


@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr)


@register.filter
def get_key(obj, key):
    return obj.get(key)


@register.simple_tag
def get_facet_verbose_name(facet_field, view):
    if hasattr(view, 'facet_field_name_overrides') and facet_field in view.facet_field_name_overrides.keys():
        facet_field_name = view.facet_field_name_overrides[facet_field]
    else:
        facet_field_name = facet_field
    return capfirst(field_name(view.model, facet_field_name))
