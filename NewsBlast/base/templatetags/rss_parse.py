from django import template
from django.template.defaultfilters import stringfilter
from lxml import etree
import re

register = template.Library()

@register.filter
@stringfilter
def clean_desc(value):
    """Cleans the RSS description from Google News"""

    parser = etree.XMLParser(resolve_entities=False, recover=True)
    tree = etree.fromstring(value, parser=parser)
    html = re.compile('<.*?>')

    for element in tree.xpath('//font[@size="-1"]'):
        if etree.tostring(element) != None and '<a' not in etree.tostring(element) and '<font color' not in etree.tostring(element) and 'class=\"p\"' not in etree.tostring(element):
            return re.sub(html, '', etree.tostring(element))

    return "A description could not be parsed for this story."

@register.filter
@stringfilter
def clean_unicode(string):
    """Replace unicode in a string with ascii characters"""

    if '\\u2018' in string:
        string = string.replace('\\u2018', '\'')
    if '\\u2019' in string:
        string = string.replace('\\u2019', '\'')
    if '\\u201c' in string:
        string = string.replace('\\u201c', '\"')
    if '\\u201d' in string:
        string = string.replace('\\u201d', '\"')
    if '\\xa0' in string:
        string = string.replace('\\xa0', ' ')
    if '\'' in string:
        string = string.replace('\'', '')
    if '&#8212;' in string:
        string = string.replace('&#8212;', '--')
    if '&#8220;' in string:
        string = string.replace('&#8220;', '"')
    if '&#8221;' in string:
        string = string.replace('&#8221;', '"')

    return string