from django import template
from content.models import Post, Comment

register = template.Library()

@register.filter
def isinstance(value, class_name):
    if class_name == 'Post':
        return isinstance(value, Post)
    elif class_name == 'Comment':
        return isinstance(value, Comment)
    return False
