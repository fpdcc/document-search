from django.template import Library

register = Library()


@register.simple_tag
def set_param(parameters, param, value):
    """
    Update query parameters for a page to set the parameter 'param' to 'value',
    returning a valid query string.

    :param parameters: A string of query parameters.
    :param param: The query parameter to update.
    :param value: The value to set for the query parameter.
    :return: The updated query string.
    """
    params = parameters.copy()
    params[param] = value
    return params.urlencode()
