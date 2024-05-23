from django.db import models
from menu.models import Menu
from reservation.models import Reservation

# Create your models here.
class Order(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)