from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BarberShop, Appointment

admin.site.register(BarberShop)
admin.site.register(Appointment)
