from django.db import models
from table.models import Table
from account.models import Account

# Create your models here.
class Reservation(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    people_count = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    is_activated = models.BooleanField()
    
class Payment(models.Model):
    order_id = models.CharField(max_length=100)
    order_type = models.CharField(max_length=100)
    amount = models.IntegerField()
    order_desc = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='pending')