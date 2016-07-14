from django.contrib import admin

from .models import Profile, Employee, DocumentModel


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'profile_id')

admin.site.register(Profile)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DocumentModel)
