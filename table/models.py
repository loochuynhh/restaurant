from django.db import models

# Create your models here.
class Table(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()