from django import template

register = template.Library()


@register.filter
def concat(a, b):
    return str(a) + str(b)


@register.filter
def display_array(obj):
    return str(obj).replace('[', '').replace(']', '')


@register.filter
def display_range(obj):
    if obj:
        # Postgres range fields are always non-inclusive on the upper bound,
        # so take this into account when checking if the bounds are the same
        lower_bound, upper_bound = obj.lower, obj.upper-1
        if lower_bound == upper_bound:
            # This is a single-value range, so display it as an integer
            return lower_bound
        else:
            return f'{lower_bound}-{upper_bound}'
    else:
        return obj
