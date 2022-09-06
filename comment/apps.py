from django.apps import AppConfig


class CommentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comment'

    def ready(self):
        super(CommentConfig, self).ready()
        from . import signals