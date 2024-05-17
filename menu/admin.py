from django.contrib import admin
from menu.models import Menu
from django.utils.html import format_html

# Register your models here.
class MenuAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image_tag.short_description = 'Review'
    image_tag.allow_tags = True
    def food_or_drink(self, obj):
        return 'Món ăn' if obj.type else 'Đồ uống'
    food_or_drink.short_description = 'Type'
    # list_display = [field.name for field in Menu._meta.fields]
    list_display = ['name','image_tag', 'food_or_drink', 'description', 'price']
    readonly_fields = ['image_tag']
    
admin.site.register(Menu, MenuAdmin)