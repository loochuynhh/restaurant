from django.db import models

# Create your models here.
class SpecialEvent(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    image = models.ImageField(upload_to='assets/images/')