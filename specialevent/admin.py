from django.contrib import admin

# Register your models here.
from specialevent.models import SpecialEvent
from django.utils.html import format_html

# Register your models here.
class SpecialEventAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image_tag.short_description = 'Review'
    list_display = [field.name for field in SpecialEvent._meta.fields]
    readonly_fields = ['image_tag']
    
admin.site.register(SpecialEvent, SpecialEventAdmin)