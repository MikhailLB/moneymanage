from django import template
from urllib.parse import urlencode
register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return round((float(value) * float(arg)), 2)
    except (ValueError, TypeError):
        return 0

