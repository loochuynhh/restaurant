from django.contrib import admin
from menu.models import Menu
from django.utils.html import format_html

# Register your models here.
class MenuAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image_tag.short_description = 'Review'
    image_tag.allow_tags = True
    list_display = [field.name for field in Menu._meta.fields]
    readonly_fields = ['image_tag']
    
admin.site.register(Menu, MenuAdmin)