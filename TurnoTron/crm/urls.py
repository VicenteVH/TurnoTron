from django.urls import path
from . import views
from .views import reserve_appointment, appointment_success, appointment_detail, cancel_appointment, modify_appointment, appointment_list


urlpatterns = [
    path('', views.homepage, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('user-logout', views.user_logout, name="user-logout"),
    path('reserve/', reserve_appointment, name='reserve_appointment'),
    path('success/', appointment_success, name='appointment_success'),
    path('appointment/<int:appointment_id>/', appointment_detail, name='appointment_detail'),
    path('appointment/<int:appointment_id>/cancel/', cancel_appointment, name='cancel_appointment'),
    path('appointment/<int:appointment_id>/modify/', modify_appointment, name='modify_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/history/', views.appointment_history, name='appointment_history'),
]









