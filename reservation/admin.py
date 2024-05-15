from django.contrib import admin

# Register your models here.
from reservation.models import Reservation

# Register your models here.
class ReservationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Reservation._meta.fields]
    
admin.site.register(Reservation, ReservationAdmin)