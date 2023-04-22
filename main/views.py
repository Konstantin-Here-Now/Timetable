import json

from django.shortcuts import render

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
