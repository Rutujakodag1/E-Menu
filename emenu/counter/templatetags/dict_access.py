# dict_access.py
from django import template

register = template.Library()

@register.filter
def dict_access(dictionary, key):
    return dictionary.get(key)
