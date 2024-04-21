from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import Appointment, BarberShop, User

# Formulario para crear/registrarse un usuario
class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Formulario para autenticar un usuario
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

# Formulario para reservar turnos
class AppointmentForm(forms.ModelForm):
    barber_shop = forms.ModelChoiceField(queryset=BarberShop.objects.all())

    class Meta:
        model = Appointment
        fields = ['barber_shop', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
