from django import template

register = template.Library()

@register.filter
def get_value_from_dict(dictionary, key):
    return dictionary.get(key)
