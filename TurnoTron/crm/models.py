#Reserva de turnos
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class BarberShop(models.Model):
    name = models.CharField(max_length=100)
    opening_time = models.TimeField(default=time(8, 0)) # Por default empieza a las 8am.
    closing_time = models.TimeField(default=time(17, 0)) # Por default cierra a las 5pm.

    def __str__(self):
        return self.name

class Appointment(models.Model):
    barber_shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE, default='1')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    issued_date = models.DateTimeField(default=timezone.now)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment #{self.pk} in {self.barber_shop} by {self.customer}"

    def cancel(self):
        self.delete()

    def modify(self, date, time):
        self.date = date
        self.time = time
        self.save()

    def get_details(self):
        return {
            'barber_shop': self.barber_shop,
            'customer': self.customer,
            'date': self.date,
            'time': self.time,
            'appointment_id': self.appointment_id,
            'issued_date': self.issued_date
        }