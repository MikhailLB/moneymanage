from django import template
from datetime import date
register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.simple_tag(name='get_current_date')
def get_current_date():
    return date.today()
@register.filter
def divide(value, divisor):
    try:
        return value / divisor
    except (ValueError, ZeroDivisionError):
        return 0