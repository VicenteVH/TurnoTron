from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment
from django.utils import timezone
from datetime import date, datetime, time
from django.contrib import messages

# - Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from .models import Customer

def homepage(request):

    return render(request, 'crm/index.html')


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)
            return redirect("my-login")

    context = {'registerform': form}
    return render(request, 'crm/register.html', context=context)


def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")


    context = {'loginform':form}

    return render(request, 'crm/my-login.html', context=context)


def user_logout(request):

    auth.logout(request)

    return redirect("")



@login_required(login_url="my-login")
def dashboard(request):

    return render(request, 'crm/dashboard.html')

# Reserva de turnos

@login_required
def reserve_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # Verificar si la fecha de la reserva es posterior a la fecha actual
            if appointment.date < timezone.now().date():
                # Si la fecha es anterior a la actual, mostrar un mensaje de error
                return render(request, 'error.html', {'message': 'La fecha de la reserva no puede ser anterior a la fecha actual.'})
            # Verificar si la fecha está dentro del horario operacional de la barberia.
            if not appointment.barber_shop.opening_time <= appointment.time <= appointment.barber_shop.closing_time:
                message = f"La hora de la reserva debe estar dentro del horario laboral de {appointment.barber_shop}\
                  ({appointment.barber_shop.opening_time.strftime('%I:%M %p')} - {appointment.barber_shop.closing_time.strftime('%I:%M %p')}"
                return render(request, 'error.html', {'message': message})
            # Verificar si la hora de la reserva es con al menos 1 hora de anticipación
            if appointment.date == timezone.now().date() and appointment.time <= (timezone.now() + timezone.timedelta(hours=1)).time():
                # Si la hora es con menos de 1 hora de anticipación, mostrar un mensaje de error
                return render(request, 'error.html', {'message': 'Debe hacer una reserva con al menos 1 día de anticipación.'})
            # Verificar si ya existe una reserva para la misma fecha y hora
            existing_appointment = Appointment.objects.filter(date=appointment.date, time=appointment.time).exists()
            if existing_appointment:
                # Si ya existe una reserva para la misma fecha y hora, mostrar un mensaje de error
                return render(request, 'error.html', {'message': 'Ya existe una reserva para esta fecha y hora.'})
            # Si todas las condiciones son satisfactorias, guardar la reserva
            appointment.customer = request.user
            appointment.issued_date = timezone.now()
            appointment.save()
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    return render(request, 'reserve_appointment.html', {'form': form})

@login_required
def appointment_success(request):
    return render(request, 'appointment_success.html')

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    in_history = False
    if appointment.date < date.today():
        in_history = True
    return render(request, 'appointment_detail.html', {'appointment': appointment})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        # Verificar si se confirma la cancelación
        if 'confirm_cancel' in request.POST:
            appointment.delete()
            return render(request, 'appointment_cancel_success.html')
        else:
            # Si no se confirma, redireccionar a otra página o mostrar un mensaje de cancelación
            return redirect('appointment_detail', appointment_id=appointment_id)

    return render(request, 'cancel_appointment.html', {'appointment': appointment}) 

@login_required
def modify_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            new_appointment = form.save(commit=False)
            if new_appointment.date < timezone.now().date() or \
                (new_appointment.date == timezone.now().date() and new_appointment.time < (timezone.now() + timezone.timedelta(hours=1)).time()):
                return render(request, 'error.html', {'message': 'No puedes modificar la reserva con una fecha u hora pasada.'})
            if Appointment.objects.exclude(pk=appointment_id).filter(date=new_appointment.date, time=new_appointment.time).exists():
                return render(request, 'error.html', {'message': 'Ya existe una reserva para la fecha y hora seleccionadas.'})
            
            new_appointment.save()
            return render(request, 'appointment_modify_success.html')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'modify_appointment.html', {'form': form, 'appointment_id': appointment_id})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment_list.html', {'appointments': appointments})

@login_required
def appointment_history(request):
    # Obtener las reservas que ya han pasado su fecha y hora
    past_appointments = Appointment.objects.filter(date__lt=timezone.now().date(), customer=request.user)
    return render(request, 'appointment_history.html', {'past_appointments': past_appointments})

@login_required
def appointment_upcoming(request):
    upcoming_appointments = Appointment.objects.filter(date__gte=date.today(), customer=request.user).order_by('date', 'time')
    return render(request, 'appointment_upcoming.html', {'upcoming_appointments': upcoming_appointments})
