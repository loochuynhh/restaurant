from django.contrib import admin

# Register your models here.
from aboutUs.models import AboutUs
from django.utils.html import format_html

# Register your models here.
class AboutUsAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image_tag.short_description = 'Review'
    list_display = ['name', 'datetime', 'image_tag','type', 'description']
    readonly_fields = ['image_tag']
    
admin.site.register(AboutUs, AboutUsAdmin)