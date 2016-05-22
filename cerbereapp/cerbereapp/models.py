from django.db import models
from django.contrib.auth.models import User, Group

#Extend User
class Account(models.Model):
    email = models.EmailField
    username = models.CharField(max_length=50)
    account_type = models.ForeignKey('AccountType')
    def __str__(self):
        return self.username

#Extend Group
class AccountType(models.Model):
    account_type_name = models.CharField(max_length=50)
    account_type_desc = models.CharField(max_length=50)
    def __str__(self):
        return self.account_type_name

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_id = models.ForeignKey('Account')
    profile_id = models.ForeignKey('Profile')
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Profile(models.Model):
    user_id = models.ForeignKey('Account')
    profile_name = models.CharField(max_length=50)
    def __str__(self):
        return self.profile_name

class DocumentModel(models.Model):
    user_id = models.ForeignKey('Account')
    document_model_name = models.CharField(max_length=50)
    profiles = models.ManyToManyField(Profile)
    warning_days = models.IntegerField
    critical_days = models.IntegerField
    def __str__(self):
        return self.document_model_name

class Document(models.Model):
    employee_id = models.ForeignKey('Employee')
    document_file = models.BinaryField
    expiration_date = models.DateField
    def __str__(self):
        return self.DocumentModel.document_model_name
