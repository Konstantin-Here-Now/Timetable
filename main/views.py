import json

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Lesson
from .forms import LessonCreateForm, LessonUpdateForm, UserRegistrationForm, UserLoginForm

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from .dates_and_time import TODAY, update

CONTACTS = {
    'name': 'Иван Щербаков',
    'phone': '+79154779740',
    'email': 'pochtynet@mail.ru',
    'vk': 'https://vk.com/id315090966',
}


def index(request):
    with open('main/dates_and_time.json', 'r', encoding='UTF-8') as dates_f:
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
            print(f'{user.username} registered!')
            user.save()
            # login(request, user)
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
            print(f'{user.username} logs in!')
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'main/users/login.html', {'form': form})


def user_logout(request):
    print(f'{request.user.username} logs out!')
    logout(request)
    return redirect('index')


def profile(request):
    user = request.user
    return render(request, 'main/users/profile.html', context={'user': user})


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonCreateForm
    template_name = 'main/enroll.html'
    context_object_name = 'form'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.pupil = self.request.user
        print(form.instance.time_lesson)
        return super().form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LessonListView(ListView):
    model = Lesson
    template_name = 'main/lessons_list.html'
    context_object_name = 'lessons'
    pk_url_kwarg = 'lesson_id'

    paginate_by = 5

    def get_queryset(self):
        return Lesson.objects.filter(date_lesson__gte=TODAY).order_by('-date_lesson')


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonUpdateForm
    template_name = 'main/lesson_update.html'
    context_object_name = 'form'

    def get_success_url(self):
        update()
        return reverse_lazy('lessons_list')

