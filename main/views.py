import logging
from datetime import datetime

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from main.business_logic.update_time import update
from .business_logic.days_dataset import get_days_dataset
from .business_logic.time_range import TimeRange
from .forms import LessonCreateForm, LessonUpdateForm, UserRegistrationForm, UserLoginForm, ContactForm
from .models import Lesson

logger = logging.getLogger(__name__)


def index(request):
    days_dataset = get_days_dataset()
    context = {'days_dataset': days_dataset}
    return render(request, 'main/index.html', context)


def contacts(request):
    context = settings.CONTACTS
    return render(request, 'main/contacts.html', context)


def faq(request):
    context = {'context': settings.FAQ}
    return render(request, 'main/faq.html', context)


def mail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_ADMIN],
                fail_silently=False
            )
            logger.info("User has just sent mail to administrator.")
        return redirect("index")

    form = ContactForm()
    return render(request, "main/mail.html", {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            logger.info(f'{user.username} registered!')
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f'{user.username} logs in!')
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'main/users/login.html', {'form': form})


def user_logout(request):
    logger.info(f'{request.user.username} logs out!')
    logout(request)
    return redirect('index')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'main/users/password_reset/password_reset.html'
    email_template_name = 'main/users/password_reset/password_reset_email.html'
    subject_template_name = 'main/users/password_reset/password_reset_subject.txt'
    success_message = 'Мы отправили письмо с дальнейшими инструкциями по смене пароля'
    success_url = reverse_lazy('index')


@login_required
def profile(request):
    user = request.user
    lessons = Lesson.objects.filter(user_id=user.id, date_lesson__gte=datetime.today()).order_by('date_lesson')

    paginator = Paginator(lessons, 3)
    pag_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(pag_num)

    context = {
        'user': user,
        'lessons': lessons,
        'page_obj': page_objects
    }
    return render(request, 'main/users/profile.html', context=context)


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonCreateForm
    template_name = 'main/enroll.html'
    context_object_name = 'form'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        pupil = self.request.user
        date_lesson = form.instance.date_lesson
        time_lesson = f'{form.instance.time_lesson_start} - {form.instance.time_lesson_end}'

        form.instance.user = pupil
        logger.info(f'{pupil} created lesson request at {date_lesson} {time_lesson}')

        # Sending email to settings.EMAIL_ADMIN
        message_to_send = f'{pupil.first_name} {pupil.last_name} предложил(-а) провести занятие {date_lesson} ' \
                          f'в промежуток {time_lesson}.'
        additional_message = form.instance.desc
        if additional_message:
            message_to_send += f'\nУченик оставил следующее сообщение:\n {additional_message}'
        else:
            message_to_send += f'\nУченик не оставил дополнительных сообщений.'
        send_mail(
            subject='Новая запись на занятие',
            message=message_to_send,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_ADMIN],
            fail_silently=False
        )
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LessonListView(ListView):
    model = Lesson
    template_name = 'main/lessons_list.html'
    context_object_name = 'lessons'
    pk_url_kwarg = 'lesson_id'

    paginate_by = 6

    def get_queryset(self):
        return Lesson.objects.filter(date_lesson__gte=datetime.today()).order_by('date_lesson')

    @method_decorator(permission_required('main.view_lesson'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonUpdateForm
    template_name = 'main/lesson_update.html'
    context_object_name = 'form'

    def form_valid(self, form):
        pupil = form.instance.user
        time_lesson = f'{form.instance.time_lesson_start} - {form.instance.time_lesson_end}'
        date_lesson = form.instance.date_lesson
        approved = 'APPROVED' if form.instance.approved is True else 'DISAPPROVED'
        logger.info(f'<<{approved}>> {pupil} {time_lesson} {date_lesson}')
        if approved == 'APPROVED':
            update(date_lesson, TimeRange(time_lesson))
            send_mail(
                subject='Ваше занятие одобрено',
                message=f'Одобрено занятие {date_lesson} в промежуток {time_lesson}.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[pupil.email],
                fail_silently=False
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lessons_list')

    @method_decorator(permission_required('main.change_lesson'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
