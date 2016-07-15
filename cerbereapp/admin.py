from django.contrib import admin

from .models import Profile, Employee, DocumentModel, AccountType


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'profile_id')


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'limit_employees', 'notifications')

admin.site.register(Profile)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DocumentModel)
admin.site.register(AccountType, AccountTypeAdmin)
