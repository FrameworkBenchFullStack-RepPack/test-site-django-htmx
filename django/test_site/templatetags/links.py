
from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag("partials/links.html")
def render_links():
    return {"NAV_LINKS": settings.NAV_LINKS}