from io import StringIO
import pprint as pretty_print

from django import template

register = template.Library()

@register.filter
def pprint(d):
    s = StringIO()
    pretty_print.pprint(d, s, indent=4)
    return s.getvalue()

@register.filter
def space2underscore(v):
    return v.replace(' ','_')

# For the template to find the conversion from keyword to label
from ..conf import FILTERING_TERMS
@register.filter
def convert2label(kw):
    return FILTERING_TERMS.get(kw)
