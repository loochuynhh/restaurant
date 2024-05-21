from django.contrib import admin

# Register your models here.
from reservation.models import Reservation
from reservation.models import Payment

# Register your models here.
class ReservationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Reservation._meta.fields]
    
admin.site.register(Reservation, ReservationAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]
    
admin.site.register(Payment, PaymentAdmin)