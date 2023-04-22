from django.db import models


class Lesson(models.Model):
    date_lesson = models.DateField(blank=False, null=False, verbose_name='Дата занятия')
    pupil_name = models.CharField(max_length=120, blank=False, null=False, default='Ученик', verbose_name='Имя ученика')
    desc = models.TextField(blank=True, null=False, verbose_name='Описание')
    date_created = models.DateField(auto_now_add=True, verbose_name='Дата создания записи')
    approved = models.BooleanField(default=False, null=False, verbose_name='Одобрено?')

    def __str__(self):
        return f'{self.pupil_name} - {self.date_lesson} - {self.date_lesson}'

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['date_lesson', 'pupil_name']
