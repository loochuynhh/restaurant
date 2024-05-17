from django.db import models
from table.models import Table
from account.models import Account

# Create your models here.
class Reservation(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    people_count = models.IntegerField()
    total_price = models.IntegerField(null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    is_activated = models.BooleanField(default=False)