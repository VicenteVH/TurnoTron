from django.contrib import admin
from .models import BarberShop

# Registro de modelos para el panel de administración
# Se importa el modelo BarberShop desde el archivo models.py
# y se registra en el panel de administración de Django para que pueda ser administrado desde allí.
admin.site.register(BarberShop)
