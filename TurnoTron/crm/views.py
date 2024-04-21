from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from .forms import AppointmentForm, CreateUserForm, LoginForm
from .models import Appointment, Customer, Barber, BarberShop
from django.utils import timezone
from datetime import date, datetime, time
from django.contrib import messages
from django.contrib.auth import authenticate

# - Authentication models and functions

from django.contrib.auth.models import auth
from django.utils import timezone
from datetime import date


# Vista para la página de inicio
def homepage(request):
    return render(request, 'crm/index.html')


# Vista para el registro de usuario
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


# Vista para el inicio de sesión del usuario
def my_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            auth.login(request, user)
            return redirect("dashboard")

    return render(request, 'crm/my-login.html')


# Vista para cerrar la sesión del usuario
def user_logout(request):
    auth.logout(request)
    return redirect("")


# Vista para el dashboard del usuario
@login_required(login_url="my-login")
def dashboard(request):
    if request.user.username not in [barber.user.username for barber in Barber.objects.all()]:
        print("Its a costumer")
        return render(request, 'crm/dashboard.html')
    else:
        print("Its a barber")
        return render(request, 'crm/barbershop_dashboard.html')


# Reserva de turnos
@login_required
def reserve_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if appointment.date < timezone.now().date():
                return render(request, 'error.html', {'message': 'La fecha de la reserva no puede ser anterior a la fecha actual.'})
            # Verificar si la fecha está dentro del horario operacional de la barberia.
            if not appointment.barber_shop.opening_time <= appointment.time <= appointment.barber_shop.closing_time:
                message = f"La hora de la reserva debe estar dentro del horario laboral de {appointment.barber_shop}\
                  ({appointment.barber_shop.opening_time.strftime('%I:%M %p')} - {appointment.barber_shop.closing_time.strftime('%I:%M %p')}"
                return render(request, 'error.html', {'message': message})
            # Verificar si la hora de la reserva es con al menos 1 hora de anticipación
            if appointment.date == timezone.now().date() and appointment.time <= (timezone.now() + timezone.timedelta(hours=1)).time():
                return render(request, 'error.html', {'message': 'Debe hacer una reserva con al menos 1 día de anticipación.'})
            existing_appointment = Appointment.objects.filter(date=appointment.date, time=appointment.time).exists()
            if existing_appointment:
                return render(request, 'error.html', {'message': 'Ya existe una reserva para esta fecha y hora.'})
            appointment.customer = request.user
            appointment.issued_date = timezone.now()
            appointment.save()
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    return render(request, 'reserve_appointment.html', {'form': form})


# Vista para mostrar un mensaje de éxito después de reservar un turno
@login_required
def appointment_success(request):
    return render(request, 'appointment_success.html')


# Vista para mostrar los detalles de una reserva
@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    in_history = False
    if appointment.date < date.today():
        in_history = True
    return render(request, 'appointment_detail.html', {'appointment': appointment})


# Vista para cancelar una reserva
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        if 'confirm_cancel' in request.POST:
            appointment.delete()
            return render(request, 'appointment_cancel_success.html')
        else:
            return redirect('appointment_detail', appointment_id=appointment_id)
    return render(request, 'cancel_appointment.html', {'appointment': appointment}) 


# Vista para modificar una reserva
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


# Vista para mostrar la lista de reservas
@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment_list.html', {'appointments': appointments})


# Vista para mostrar la lista de reservas de una barbería
def barbershop_upcoming_appointments(request):
    barbershop = request.user.barber.barbershop
    upcoming_appointments = Appointment.objects.filter(date__gte=date.today(), barber_shop=barbershop).order_by('date', 'time')

    # Pagina pedida
    page = request.GET.get("page")

    # Reservaciones por página
    APPOINTMENTS_PER_PAGE = 8

    # Paginador
    upcoming_appointments = Paginator(upcoming_appointments, APPOINTMENTS_PER_PAGE)

    try:
        upcoming_appointments = upcoming_appointments.page(page)
    except PageNotAnInteger:
        upcoming_appointments = upcoming_appointments.page(1)
    except EmptyPage:
        upcoming_appointments = upcoming_appointments.page(upcoming_appointments.num_pages)

    return render(request, 'crm/barbershop_appointment_upcoming.html', {'upcoming_appointments': upcoming_appointments})


def barbershop_appointments_history(request):
    barbershop = request.user.barber.barbershop
    # Obtener las reservas que ya han pasado su fecha y hora
    past_appointments = Appointment.objects.filter(date__lt=timezone.now().date(), barber_shop=barbershop)

    # Pagina pedida
    page = request.GET.get("page")

    # Reservaciones por página
    APPOINTMENTS_PER_PAGE = 8

    # Paginador
    past_appointments = Paginator(past_appointments, APPOINTMENTS_PER_PAGE)

    try:
        past_appointments = past_appointments.page(page)
    except PageNotAnInteger:
        past_appointments = past_appointments.page(1)
    except EmptyPage:
        past_appointments = past_appointments.page(past_appointments.num_pages)

    return render(request, 'crm/barbershop_appointment_history.html', {'past_appointments': past_appointments})


# Vista para mostrar el historial de reservas pasadas
@login_required
def appointment_history(request):
    # Obtener las reservas que ya han pasado su fecha y hora
    past_appointments = Appointment.objects.filter(date__lt=timezone.now().date(), customer=request.user)

    # Pagina pedida
    page = request.GET.get("page")

    # Reservaciones por página
    APPOINTMENTS_PER_PAGE = 6

    # Paginador
    past_appointments = Paginator(past_appointments, APPOINTMENTS_PER_PAGE)

    try:
        past_appointments = past_appointments.page(page)
    except PageNotAnInteger:
        past_appointments = past_appointments.page(1)
    except EmptyPage:
        past_appointments = past_appointments.page(past_appointments.num_pages)
    
    return render(request, 'appointment_history.html', {'past_appointments': past_appointments})


# Vista para mostrar las próximas reservas
@login_required
def appointment_upcoming(request):
    upcoming_appointments = Appointment.objects.filter(date__gte=date.today(), customer=request.user).order_by('date', 'time')

    # Pagina pedida
    page = request.GET.get("page")

    # Reservaciones por página
    APPOINTMENTS_PER_PAGE = 6

    # Paginador
    upcoming_appointments = Paginator(upcoming_appointments, APPOINTMENTS_PER_PAGE)

    try:
        upcoming_appointments = upcoming_appointments.page(page)
    except PageNotAnInteger:
        upcoming_appointments = upcoming_appointments.page(1)
    except EmptyPage:
        upcoming_appointments = upcoming_appointments.page(upcoming_appointments.num_pages)

    return render(request, 'appointment_upcoming.html', {'upcoming_appointments': upcoming_appointments})
