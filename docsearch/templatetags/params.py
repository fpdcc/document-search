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


@register.simple_tag
def set_facet_param(parameters, facet, value):
    """
    Update query parameters for a page to set the facet 'facet' to 'value',
    returning a valid query string.

    :param parameters: A string of query parameters.
    :param facet: The facet parameter to update, e.g. "township_exact".
    :param value: The value to set for the facet parameter.
    :return: The updated query string.
    """
    params = parameters.copy()
    facet_str = f'{facet}:{value}'
    if facet_str not in params.getlist('selected_facets'):
        params.update({'selected_facets': facet_str})
    return params.urlencode()


@register.simple_tag
def remove_facet_param(parameters, facet, value):
    """
    Update query parameters for a page to remove the facet 'facet' with the
    given 'value', returning a valid query string.

    :param parameters: A string of query parameters.
    :param facet: The facet parameter to update, e.g. "township_exact".
    :param value: The value to remove for the facet parameter.
    :return: The updated query string.
    """
    params = parameters.copy()
    facet_str = f'{facet}:{value}'
    selected_facets = params.getlist('selected_facets')
    if facet_str in selected_facets:
        selected_facets.remove(facet_str)
        params.setlist('selected_facets', selected_facets)
    return params.urlencode()
