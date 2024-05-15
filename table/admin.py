from django.contrib import admin

# Register your models here.
from table.models import Table

# Register your models here.
class TableAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Table._meta.fields]
    
admin.site.register(Table, TableAdmin)