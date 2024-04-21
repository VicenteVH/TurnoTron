from django.urls import path
from . import views
from .views import reserve_appointment, appointment_success, appointment_detail, cancel_appointment, modify_appointment, appointment_list, appointment_history, appointment_upcoming
from django.conf import settings
from django.conf.urls.static import static

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
    path('appointments/', appointment_list, name='appointment_list'),
    path('barbershop-appointments/', views.barbershop_upcoming_appointments, name='barbershop_upcoming_appointments'),
    path('barbershop-appointments-history/', views.barbershop_appointments_history, name='barbershop_appointments_history'),
    path('appointments/<int:appointment_id>/', appointment_detail, name='appointment_detail'),
    path('appointment-history/', appointment_history, name='appointment_history'),
    path('appointment-upcoming/', appointment_upcoming, name='appointment_upcoming'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
