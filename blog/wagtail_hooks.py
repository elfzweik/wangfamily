from wagtail.core import hooks
from django.conf import settings
from django.utils.html import format_html


@hooks.register("insert_global_admin_css")
def import_fontawesome_stylesheet():
    elem = '<link rel="stylesheet" href="{}/fontawesome-free-5.15.4-web/css/font-awesome.min.css">'.format(
        settings.STATIC_URL
    )
    return format_html(elem)