from django import template

register = template.Library()


@register.filter
def subtract(obj, arg):
    return obj - arg


@register.filter
def absubtract(obj, arg):
    return abs(obj - arg)
