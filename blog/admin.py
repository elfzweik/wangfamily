from django.contrib import admin
from .models import *

@admin.register(BlogDetailPage)
class BlogDetailPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'custom_title', 'author', 'create_date', 'update_date', 'intro',  'content')
