from django.contrib import admin

from .models import Profile, Employee, DocumentModel

admin.site.register(Profile)
admin.site.register(Employee)
admin.site.register(DocumentModel)
