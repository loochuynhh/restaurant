from django.contrib import admin

from comment.models import Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]
    readonly_fields = [field.name for field in Comment._meta.fields]
    def has_change_permission(self, request, obj=None):
        return False  # Ngăn admin thay đổi bản ghi
    def has_add_permission(self, request):
        return False
admin.site.register(Comment, CommentAdmin)