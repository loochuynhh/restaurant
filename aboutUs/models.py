from django.db import models

# Create your models here.
class AboutUs(models.Model):
    TYPE_CHOICES = [
        ('Pic', 'Hình ảnh'),
        ('Rep', 'Bài viết'),
        ('Sta', 'Nhân viên'),
    ]
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    datetime = models.DateTimeField()
    image = models.ImageField(upload_to='assets/images/')
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
