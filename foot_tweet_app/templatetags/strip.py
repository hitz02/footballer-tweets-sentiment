from django import template

register = template.Library()

@register.filter
def stripp(s):
    return s.strip('@')
