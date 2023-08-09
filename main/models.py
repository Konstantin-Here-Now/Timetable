from typing import Union, Literal

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    date_lesson = models.DateField(blank=False, null=False, verbose_name='Дата занятия')
    time_lesson_start = models.TimeField(blank=False, null=False, verbose_name='Начало занятия')
    time_lesson_end = models.TimeField(blank=False, null=False, verbose_name='Конец занятия')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    desc = models.TextField(blank=True, null=False, verbose_name='Описание')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    approved = models.BooleanField(default=False, null=False, verbose_name='Одобрено?')

    def __str__(self):
        return f'{self.user} : {self.date_lesson} : {self.time_lesson_start} - {self.time_lesson_end}'

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['date_lesson', 'time_lesson_start', 'date_created']


class AvailableTimeModel(models.Model):
    class TimeType(models.TextChoices):
        DEFAULT = "default"
        ACTUAL = "actual"

    time_type: Literal["default", "actual"] = models.CharField(primary_key=True, max_length=7, choices=TimeType.choices,
                                                               verbose_name="Тип времени")
    monday = models.CharField(max_length=80, blank=False, null=False, verbose_name="Понедельник")
    tuesday = models.CharField(max_length=80, blank=False, null=False, verbose_name="Вторник")
    wednesday = models.CharField(max_length=80, blank=False, null=False, verbose_name="Среда")
    thursday = models.CharField(max_length=80, blank=False, null=False, verbose_name="Четверг")
    friday = models.CharField(max_length=80, blank=False, null=False, verbose_name="Пятница")
    saturday = models.CharField(max_length=80, blank=False, null=False, verbose_name="Суббота")
    sunday = models.CharField(max_length=80, blank=False, null=False, verbose_name="Воскресенье")

    def __str__(self):
        return f'{self.time_type} time'

    class Meta:
        verbose_name = 'Свободное время'
        verbose_name_plural = 'Свободное время'
