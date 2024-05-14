from django.db import models
from table.models import Table

# Create your models here.
class Reservation(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    people_count = models.IntegerField()
    total_price = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)