from django import template

register = template.Library()


@register.filter
def make_range(x):
    return range(x)
