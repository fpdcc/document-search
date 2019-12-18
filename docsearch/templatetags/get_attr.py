from django import template

register = template.Library()


@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr)


@register.filter
def get_key(obj, key):
    return obj.get(key)
