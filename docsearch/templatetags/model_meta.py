from django import template

register = template.Library()


@register.filter
def verbose_name(obj):
    """
    Return the verbose_name for a Model in a template. This filter is necessary
    because Django considers the Meta Options to be private, and hence
    not accessible in templates.
    """
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


@register.filter
def field_name(value, field):
    """
    Return the verbose fieldname for a given 'field' on an object or Model.
    """
    Model = value.model if hasattr(value, 'model') else value
    return Model._meta.get_field(field).verbose_name
