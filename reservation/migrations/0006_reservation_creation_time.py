# Generated by Django 5.0.4 on 2024-05-16 08:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_alter_reservation_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
