from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from notifications.signals import notify
from .models import LikeRecord


@receiver(post_save, sender=LikeRecord)
def send_notification(sender, instance, **kwargs):
    if instance.content_type.model == 'blogdetailpage':
        blog = instance.content_object
        verb = '点赞了你的《{0}》'.format(blog.title)
        #.format( blog.title)
    elif instance.content_type.model == 'mycomment':
        comment = instance.content_object
        verb = '点赞了你的评论“{0}”'.format( 
                strip_tags(comment.text)
            )

    recipient = instance.content_object.get_user()
    url = instance.content_object.get_url()
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)