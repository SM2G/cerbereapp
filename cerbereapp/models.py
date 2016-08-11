# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User, Group


class AccountType(models.Model):
    user_id = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    limit_employees = models.IntegerField(default=5)
    notifications = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DocumentModel(models.Model):
    user_id = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    warning_days = models.IntegerField(default=2)
    critical_days = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user_id = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    documentmodels_list = models.ManyToManyField(DocumentModel,default=None, blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    user_id = models.ForeignKey(User)
    profile_id = models.ForeignKey('Profile')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_employee_documents(self):
        return ActualDocument.objects.get(employee=self.id)

    def check_employee(self):
        # Adding
        current_employee = self.id
        current_profile = Profile.objects.get(id=self.profile_id.id)
        for document_to_have in current_profile.documentmodels_list.all():
            print('======= document:',document_to_have, end=' ')
            try:
                ActualDocument.objects.get(documentmodel=document_to_have, employee=current_employee)
                print('OK!')
            except:
                print('-NOT- OK!', end=' ')
                new_document = ActualDocument(employee=self,documentmodel=document_to_have)
                new_document.save()
                print('>>>>>>> New document saved.')
        # Cleaning
        authorized_document_models = []
        for document_model in current_profile.documentmodels_list.all():
            authorized_document_models.append(document_model.id)
        print('authorized list', authorized_document_models)
        check_documents = ActualDocument.objects.filter(employee=self).all()
        for check_document in check_documents:
            if check_document.documentmodel.id not in authorized_document_models:
                print('Document',check_document.id,end=' ')
                check_document.delete()
                print('>>>>>>> has been DESTROYED!!!')
            else:
                print('Document',check_document.id,'is good.')

    def get_employee_status(self):
        expired_counter = 0
        critical_counter = 0
        warning_counter = 0
        print('======= Checking employee',self,'...')
        for document in ActualDocument.objects.all().filter(employee=self):
            document_status = document.get_document_status()
            if document_status == 'expired':
                expired_counter += 1
            if document_status == 'critical':
                critical_counter += 1
            if document_status == 'warning':
                warning_counter += 1

        # Check if expired
        if expired_counter > 0:
            print('EXPIRED !!!')
            employee_status = 'expired'
        # Check if critical
        elif critical_counter > 0:
            print('Critical !!')
            employee_status = 'critical'
        # Check if warning
        elif warning_counter > 0:
            print('Warning !')
            employee_status = 'warning'
        else:
            print('Ok.')
            employee_status = 'valid'
        return employee_status

    class Meta:
        ordering = ["-is_active","last_name"]


class ActualDocument(models.Model):
    employee = models.ForeignKey(Employee)
    documentmodel = models.ForeignKey(DocumentModel)
    document_file = models.FileField(null=True, blank=True, upload_to="self.employee.id/self.documentmodel")
    expiration_date = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.documentmodel.name

    def get_document_status(self):
        today = datetime.date.today()
        expiration_date = self.expiration_date
        critical_treshold = timedelta(days = self.documentmodel.critical_days)
        warning_treshold = timedelta(days = self.documentmodel.warning_days)
        print('======= Document',self,'expires on',self.expiration_date,'is', end=' ')
        # Check if expired
        if expiration_date <= today:
            print('EXPIRED !!!')
            document_status = 'expired'
        # Check if critical
        elif (expiration_date - today) <= critical_treshold:
            print('Critical !!')
            document_status = 'critical'
        # Check if warning
        elif (expiration_date - today) <= warning_treshold:
            print('Warning !')
            document_status = 'warning'
        else:
            print('Ok.')
            document_status = 'valid'
        return document_status
