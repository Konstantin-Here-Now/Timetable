from django.contrib import admin
from .models import Lesson, AvailableTime


class LessonAdmin(admin.ModelAdmin):
    list_display = ('date_lesson', 'user', 'desc', 'approved')
    list_display_links = ('date_lesson',)
    search_fields = ('user', 'desc')
    list_editable = ('desc', 'approved')
    list_filter = ('date_lesson', 'user', 'desc', 'approved')


class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('time_type', )


admin.site.register(Lesson, LessonAdmin)
admin.site.register(AvailableTime, AvailableTimeAdmin)
