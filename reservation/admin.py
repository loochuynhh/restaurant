from django.contrib import admin
from .models import Reservation, Payment

<<<<<<< HEAD
# Register your models here.
from reservation.models import Reservation
from reservation.models import Payment

# Register your models here.
=======
>>>>>>> Restaurant/master
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_time', 'end_time', 'people_count', 'total_price', 'is_activated', 'get_selected_menu', 'username']
    readonly_fields = ['start_time', 'end_time', 'people_count', 'total_price', 'is_activated', 'username']

    def get_selected_menu(self, obj):
        ordered_menus = obj.order_set.all()
        return ', '.join([order.menu.name for order in ordered_menus])

    get_selected_menu.short_description = 'Ordered Menu'

    def username(self, obj):
        return obj.user.username

    username.short_description = 'Username'
    
admin.site.register(Reservation, ReservationAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]
<<<<<<< HEAD
    
admin.site.register(Payment, PaymentAdmin)
=======
    readonly_fields = [field.name for field in Payment._meta.fields]
admin.site.register(Payment, PaymentAdmin)

>>>>>>> Restaurant/master
