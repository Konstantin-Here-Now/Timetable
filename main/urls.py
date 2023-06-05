from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *
from .forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('enroll/', LessonCreateView.as_view(), name='enroll'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('password_reset/', ResetPasswordView.as_view(form_class=EmailValidationOnForgotPassword), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='main/users/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='main/users/password_reset/password_reset_complete.html'), name='password_reset_complete'),
    # path('password_reset/', password_reset, name='password_reset'),
    path('profile/', profile, name='profile'),

    path('lessons_list/', LessonListView.as_view(), name='lessons_list'),
    path('lesson_update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update')

]
