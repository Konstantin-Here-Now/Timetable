import json

from django.shortcuts import render, redirect

from .forms import NameForm, UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, logout

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


def enroll(request):
    return render(request, 'main/enroll.html')


def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return render(request, 'main/contacts.html')


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
