from django.contrib import admin

from visitor_record.models import DayNumber, Userip, VisitNumber

# Register your models here.
@admin.register(Userip)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('ip', 'location', 'count')

@admin.register(VisitNumber)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('count',)

@admin.register(DayNumber)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('day', 'count')