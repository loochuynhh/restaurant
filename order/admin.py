from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu_name', 'reservation', 'quantity']
    readonly_fields = ['menu', 'reservation', 'quantity']
    def menu_name(self, obj):
        return obj.menu.name
    
    # Đặt tên cho cột hiển thị của trường 'menu_name'
    menu_name.short_description = 'Menu Name'

admin.site.register(Order, OrderAdmin)
