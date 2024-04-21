from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BarberShop, Appointment, Barber, User

# Registro de modelos para el panel de administración
# Se importa el modelo BarberShop desde el archivo models.py
# y se registra en el panel de administración de Django para que pueda ser administrado desde allí.
admin.site.register(User)
admin.site.register(BarberShop)
admin.site.register(Appointment)
admin.site.register(Barber)
