from django import template

register = template.Library()


@register.filter
def get_item(value, key):
    if not isinstance(value, dict):
        return ""
    return value.get(str(key), "")
