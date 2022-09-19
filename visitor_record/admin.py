from django.contrib import admin

from visitor_record.models import DayNumber, Userip, VisitNumber, BlogVisitNumber

# Register your models here.
@admin.register(Userip)
class UseripAdmin(admin.ModelAdmin):
    list_display = ('ip', 'location', 'count')

@admin.register(VisitNumber)
class VisitNuberAdmin(admin.ModelAdmin):
    list_display = ('count',)

@admin.register(DayNumber)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ( 'count',)

@admin.register(BlogVisitNumber)
class BlogVisitNumberAdmin(admin.ModelAdmin):
    list_display = ('count', 'content_type', 'object_id',)