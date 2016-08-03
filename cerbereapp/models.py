# -*- coding: utf-8 -*-
import datetime
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


class ActualDocument(models.Model):
    employee = models.ForeignKey(Employee)
    documentmodel = models.ForeignKey(DocumentModel)
    document_file = models.BinaryField(null=True)
    expiration_date = models.DateField(default=datetime.date.today, blank=True)
    def __str__(self):
        return self.documentmodel.name
