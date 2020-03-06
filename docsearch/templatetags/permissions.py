from django import template
from django.contrib.auth.models import Permission

register = template.Library()


def _can_do_action(user, action, Model):
    """Helper method for checking user permissions."""
    if user.is_superuser:
        return True
    else:
        if Model is None:
            return user.groups.filter(name='Read/Write').exists()
        else:
            perms = user.user_permissions.all() | Permission.objects.filter(group__user=user)
            return perms.filter(codename='{}_{}'.format(action, Model.get_slug())).exists()


@register.filter
def can_create(user, Model=None):
    return _can_do_action(user, 'add', Model)


@register.filter
def can_update(user, Model=None):
    return _can_do_action(user, 'change', Model)


@register.filter
def can_delete(user, Model=None):
    return _can_do_action(user, 'delete', Model)
