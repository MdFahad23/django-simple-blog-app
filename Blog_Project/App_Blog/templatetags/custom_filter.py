from django import template

register = template.Library()


@register.filter(name="range_filter")
def range_filter(value):
    return value[0:500] + "............."


# register.filter("range_filter", range_filter)
