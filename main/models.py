from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    date_lesson = models.DateField(blank=False, null=False, verbose_name='Дата занятия')
    time_lesson = models.TextField(blank=False, null=False, verbose_name='Время занятия')
    pupil = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    desc = models.TextField(blank=True, null=False, verbose_name='Описание')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    approved = models.BooleanField(default=False, null=False, verbose_name='Одобрено?')

    def __str__(self):
        return f'{self.pupil} - {self.date_lesson} - {self.time_lesson}'

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['date_lesson', 'time_lesson', 'date_created']
