from django import template

register = template.Library()


@register.filter
def display_array(obj):
    return str(obj).replace('[', '').replace(']', '')
