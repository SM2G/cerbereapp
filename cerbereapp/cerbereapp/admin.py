from django.contrib import admin

from .models import Account, AccountType, Profile, Employee, DocumentModel

admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(Profile)
admin.site.register(Employee)
admin.site.register(DocumentModel)
