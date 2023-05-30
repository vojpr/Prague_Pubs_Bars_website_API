from django import template

register = template.Library()


@register.filter
def create_range(x):
    return range(x)
