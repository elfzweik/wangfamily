from django.contrib import admin
from .models import MyComment

# Register your models here.
@admin.register(MyComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'text', 'comment_time', 'user', 'root', 'parent')
