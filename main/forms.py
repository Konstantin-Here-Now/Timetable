from django import forms
from django.core.exceptions import ValidationError

from .models import Lesson
from .dates_and_time import TODAY, time_range_to_min, is_time_available

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.conf import settings


class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        # fields = ('date_lesson', 'time_lesson', 'desc')
        fields = ('date_lesson', 'desc', 'time_lesson_start', 'time_lesson_end')
        widgets = {
            'date_lesson': forms.TextInput(attrs={'class': 'form-input', 'type': 'date'}),
            'desc': forms.Textarea(
                attrs={'class': 'form-input', 'placeholder': 'Предмет для занятий, дополнительные комментарии'}),
            'time_lesson_start': forms.TimeInput(attrs={'class': 'form-input', 'placeholder': '12:00', 'type': 'time'}),
            'time_lesson_end': forms.TimeInput(attrs={'class': 'form-input', 'placeholder': '13:00', 'type': 'time'})
        }

    def clean_time_lesson_end(self):
        time_lesson_end = self.cleaned_data['time_lesson_end']
        time_lesson = f"{self.cleaned_data['time_lesson_start']} - {time_lesson_end}"
        time_lesson_range = time_range_to_min(time_lesson)
        time_lesson_hours = time_lesson_range[1] - time_lesson_range[0]
        if time_lesson_hours < 0:
            raise ValidationError('Начало занятия позже, чем его конец')
        if time_lesson_hours > settings.MAX_TIME_FOR_LESSON:
            raise ValidationError(f'Максимальная продолжительность занятия - {settings.MAX_TIME_FOR_LESSON} минут')
        if time_lesson_hours < settings.MIN_TIME_FOR_LESSON:
            raise ValidationError(f'Минимальная продолжительность занятия - {settings.MIN_TIME_FOR_LESSON} минут')

        date_lesson = self.cleaned_data['date_lesson']
        if not is_time_available(day_date=date_lesson, time_range=time_lesson):
            raise ValidationError(f'Выбранное Вами время недоступно для записи')

        return time_lesson_end

    def clean_date_lesson(self):
        date_lesson = self.cleaned_data['date_lesson']
        if date_lesson < TODAY.date():
            raise ValidationError(f'Пока машину времени не придумали, Вы не можете записаться на занятие в прошлом')
        return date_lesson


class LessonUpdateForm(LessonCreateForm):
    def __init__(self, *args, **kwargs):
        super(LessonCreateForm, self).__init__(*args, **kwargs)

    class Meta(LessonCreateForm.Meta):
        fields = ('date_lesson', 'time_lesson_start', 'time_lesson_end', 'desc', 'approved')
        widgets = LessonCreateForm.Meta.widgets


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


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "Пользователь с таким электронным адресом отсутствует."
            self.add_error('email', msg)
        return email

