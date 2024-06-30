from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Return the URL with the GET parameters, updated to reflect the passed kwargs.
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
        return d.urlencode()
