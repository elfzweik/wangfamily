from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import BlogCategory


register = template.Library()

@register.simple_tag
def get_categories():
    return BlogCategory.objects.all()