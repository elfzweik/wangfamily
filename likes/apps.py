from django.apps import AppConfig


class LikesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'likes'

    def ready(self):
        super(LikesConfig, self).ready()
        from . import signals
