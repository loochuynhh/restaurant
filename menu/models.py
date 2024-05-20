from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='assets/images/')
    type = models.BooleanField()
    description = models.CharField(max_length=200)
    price = models.IntegerField()