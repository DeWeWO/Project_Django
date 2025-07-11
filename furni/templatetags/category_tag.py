from django import template
from furni.models import Category

register = template.Library()

@register.simple_tag
def get_categories():
    return Category.objects.all().order_by("title")