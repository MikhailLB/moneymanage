from django import template
from urllib.parse import urlencode
register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return round((float(value) * float(arg)), 2)
    except (ValueError, TypeError):
        return 0


@register.filter
def humanize_timedelta(delta):

    if not delta:
        return ''

    days = delta.days
    if days == 0:
        return 'меньше дня'
    elif days == 1:
        return '1 день'
    elif 2 <= days <= 4:
        return f'{days} дня'
    else:
        return f'{days} дней'