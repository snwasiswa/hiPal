from django import template

register = template.Library()


@register.filter
def model_name(item):
    """Returns object model name"""
    try:
        return item._meta.model_name
    except AttributeError:
        return None
