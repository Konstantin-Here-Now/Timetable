from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('enroll/', LessonCreateView.as_view(), name='enroll'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('profile/', profile, name='profile'),

]