import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Lesson
from .dates_and_time import time_range_to_min

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.conf import settings


class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        # fields = ('date_lesson', 'time_lesson', 'desc')
        fields = ('date_lesson', 'desc')
        widgets = {
            'date_lesson': forms.TextInput(attrs={'class': 'form-input', 'type': 'date'}),
            'desc': forms.Textarea(
                attrs={'class': 'form-input', 'placeholder': 'Предмет для занятий, дополнительные комментарии'}),
        }

    # def clean_time_lesson(self):
    #     time_lesson = self.cleaned_data['time_lesson']
    #     if not re.fullmatch(r'\d{2}:\d{2} - \d{2}:\d{2}', time_lesson):
    #         raise ValidationError('Время записи должно иметь похожие вид: "09:00 - 10:00"')
    #     return time_lesson


class LessonUpdateForm(LessonCreateForm):
    def __init__(self, *args, **kwargs):
        super(LessonCreateForm, self).__init__(*args, **kwargs)

    class Meta(LessonCreateForm.Meta):
        fields = ('date_lesson', 'time_lesson', 'desc', 'approved')
        widgets = LessonCreateForm.Meta.widgets
        widgets['time_lesson'] = forms.TextInput(attrs={'class': 'form-input', 'placeholder': '12:00 - 13:00'})

    def clean_time_lesson(self):
        time_lesson = self.cleaned_data['time_lesson']
        time_lesson_range = time_range_to_min(time_lesson)
        time_lesson_hours = time_lesson_range[1] - time_lesson_range[0]
        if time_lesson_hours < 0:
            raise ValidationError('Начало занятия позже, чем его конец')
        if time_lesson_hours > settings.MAX_TIME_FOR_LESSON:
            raise ValidationError(f'Максимальная продолжительность занятия - {settings.MAX_TIME_FOR_LESSON} минут')
        if not re.fullmatch(r'\d{2}:\d{2} - \d{2}:\d{2}', time_lesson):
            raise ValidationError('Время записи должно иметь похожие вид: "09:00 - 10:00"')
        return time_lesson


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(min_length=3, max_length=30, label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Введите логин',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        min_length=2,
        max_length=30,
    )
    password = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
