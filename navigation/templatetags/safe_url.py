# templatetags/safe_url.py
from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.filter
def safe_url(value):
    try:
        return reverse(value)
    except NoReverseMatch:
        return "#"
