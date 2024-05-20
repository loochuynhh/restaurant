from django.contrib import admin
from account.models import Account

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Account._meta.fields]
    
admin.site.register(Account, AccountAdmin)