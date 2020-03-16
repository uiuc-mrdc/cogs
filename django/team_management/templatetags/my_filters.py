from django import template

register = template.Library()

@register.filter(name='rem_range') 
def myRange(number):
    return range(4-number)