from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import MyComment
from ..forms import CommentForm


register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    n=MyComment.objects.filter(content_type=content_type, object_id=obj.pk).count()
    return n

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={
            'content_type': content_type.model, 
            'object_id': obj.pk, 
            'reply_comment_id': 0})
    return form

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = MyComment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-update_time')

