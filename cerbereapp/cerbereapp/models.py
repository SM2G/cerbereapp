from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
User = get_user_model()
#Extend User
#class User(models.Model):
#    email = models.EmailField
#    username = models.CharField(max_length=50)
#    account_type = models.ForeignKey('AccountType')
#Extend Group
#class AccountType(models.Model):
#    account_type_name = models.CharField(max_length=50)
#    account_type_desc = models.CharField(max_length=50)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_id = models.ForeignKey('User')
    profile_id = models.ForeignKey('Profile')


class Profile(models.Model):
    user_id = models.ForeignKey('User')
    profile_name = models.CharField(max_length=50)


class DocumentModel(models.Model):
    user_id = models.ForeignKey('User')
    document_model_name = models.CharField(max_length=50)
    warning_days = models.IntegerField
    critical_days = models.IntegerField


class Document(models.Model):
    employee_id = models.ForeignKey('Employee')
    document_file = models.BinaryField
    expiration_date = models.DateField
