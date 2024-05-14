from django.db import models
from account.models import Account
from table.models import Table

# Create your models here.
class Reservation(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    people_count = models.IntegerField()
    total_price = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)