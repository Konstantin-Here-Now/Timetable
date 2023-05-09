import json
import logging

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Lesson
from .forms import LessonCreateForm, LessonUpdateForm, UserRegistrationForm, UserLoginForm

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from .dates_and_time import TODAY, DATES_JSON_PATH, update

logger = logging.getLogger(__name__)

CONTACTS = settings.CONTACTS


def index(request):
    with open(DATES_JSON_PATH, 'r', encoding='UTF-8') as dates_f:
        dates_data = json.loads(dates_f.read())
    return render(request, 'main/index.html', context={'days_dataset': dates_data})


def contacts(request):
    context = CONTACTS
    return render(request, 'main/contacts.html', context)


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


@login_required
def profile(request):
    user = request.user
    lessons = Lesson.objects.filter(pupil_id=user.id, date_lesson__gte=TODAY).order_by('date_lesson')

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
        form.instance.pupil = self.request.user
        form.instance.time_lesson = self.request.POST.get('time_start') + ' - ' + self.request.POST.get('time_end')
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AllLessonListView(ListView):
    model = Lesson
    template_name = 'main/lessons_list.html'
    context_object_name = 'lessons'
    pk_url_kwarg = 'lesson_id'

    paginate_by = 6

    def get_queryset(self):
        return Lesson.objects.filter(date_lesson__gte=TODAY).order_by('date_lesson')

    @method_decorator(permission_required('main.view_lesson'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonUpdateForm
    template_name = 'main/lesson_update.html'
    context_object_name = 'form'

    def form_valid(self, form):
        pupil = form.instance.pupil
        time_lesson = form.instance.time_lesson
        date_lesson = form.instance.date_lesson
        approved = 'APPROVED' if form.instance.approved is True else 'DISAPPROVED'
        logger.info(f'<<{approved}>> {pupil} {time_lesson} {date_lesson}')
        return super().form_valid(form)

    def get_success_url(self):
        update()
        return reverse_lazy('lessons_list')

    @method_decorator(permission_required('main.change_lesson'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
