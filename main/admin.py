from django.contrib import admin
from .models import Lesson


class LessonAdmin(admin.ModelAdmin):
    list_display = ('date_lesson', 'user', 'desc', 'approved')
    list_display_links = ('date_lesson',)
    search_fields = ('user', 'desc')
    list_editable = ('desc', 'approved')
    list_filter = ('date_lesson', 'user', 'desc', 'approved')


admin.site.register(Lesson, LessonAdmin)
