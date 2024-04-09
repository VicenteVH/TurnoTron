from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, AppointmentForm
from .models import Customer, Appointment
from django.contrib.auth import authenticate
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

# Vista para cerrar la sesión del usuario
def user_logout(request):
    auth.logout(request)
    return redirect("")

# Vista para el dashboard del usuario
@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'crm/dashboard.html')

# Vista para reservar un turno
@login_required
def reserve_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if appointment.date < timezone.now().date():
                return render(request, 'error.html', {'message': 'La fecha de la reserva no puede ser anterior a la fecha actual.'})
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

# Vista para mostrar el historial de reservas pasadas
@login_required
def appointment_history(request):
    past_appointments = Appointment.objects.filter(date__lt=timezone.now().date())
    return render(request, 'appointment_history.html', {'past_appointments': past_appointments})

# Vista para mostrar las próximas reservas
@login_required
def appointment_upcoming(request):
    upcoming_appointments = Appointment.objects.filter(date__gte=date.today()).order_by('date', 'time')
    return render(request, 'appointment_upcoming.html', {'upcoming_appointments': upcoming_appointments})
