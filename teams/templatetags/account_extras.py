from django import template
from django.template.defaultfilters import stringfilter

import ast
import datetime

register = template.Library()

@register.filter(name='string_to_list')
@stringfilter
def string_to_list(value):
    stringed_list = value
    stringed_list = ast.literal_eval(stringed_list)
    stringed_list = [n.strip() for n in stringed_list]
    return stringed_list


@register.filter
def days_left(duration):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    days_left = (duration - datetime.datetime.now().date()).days
    return days_left
