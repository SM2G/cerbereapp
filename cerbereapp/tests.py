# -*- coding: utf-8 -*-
import datetime

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import *


class CerbereAppViewsTestCase(TestCase):
    def setUp(self):
        #account_type = AccountType.objects.create(user_id=1, name="Silver")
        self.user_one = User.objects.create_user(username="user_one", email="user_one@gmail.com", password="user_one")
        self.account_type = AccountType.objects.create(user_id=self.user_one, name="Silver")
        self.account_type.save()
        self.user_one.save()

        self.user_two = User.objects.create_user(username="user_two", email="user_two@gmail.com", password="user_two")
        self.account_type = AccountType.objects.create(user_id=self.user_two, name="Silver")
        self.account_type.save()
        self.user_one.save()

        self.documentmodel_one_one = DocumentModel.objects.create(user_id=self.user_one, name="documentmodel_one_one",warning_days=10,critical_days=5)
        self.documentmodel_one_one.save()
        self.profile_one = Profile.objects.create(user_id=self.user_one, name="profile_one")
        self.profile_one.save()


## Views
## #############################################################################
    def test_view_root(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)


    def test_view_index(self):
        resp = self.client.get('/index/')
        self.assertEqual(resp.status_code, 200)


    def test_is_account_private(self):
        resp = self.client.get('/account/')
        self.assertEqual(resp.status_code, 302)


    def test_is_dashboard_private(self):
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 302)


    def test_is_employee_private(self):
        resp = self.client.get('/employees/')
        self.assertEqual(resp.status_code, 302)


## Login
## #############################################################################
    def test_false_login(self):
        self.logged_in = self.client.login(username="user_one", password="user_two")
        self.assertFalse(self.logged_in)
        resp = self.client.get('/account/')


    def test_true_login(self):
        self.logged_in = self.client.login(username="user_one", password="user_one")
        self.assertTrue(self.logged_in)
        resp = self.client.get('/account/')


## CRUD
## #############################################################################
    def test_create_documentmodel(self):
        self.logged_in = self.client.login(username="user_one", password="user_one")
        self.documentmodel_one = DocumentModel.objects.create(user_id=self.user_one, name="paper_one", warning_days=10, critical_days=5)
        self.assertTrue(self.documentmodel_one)


#    def test_create_documentmodel_critical_superior_to_warning(self):
#        self.logged_in = self.client.login(username="user_one", password="user_one")
#        self.documentmodel_false = DocumentModel.objects.create(user_id=self.user_one, name="paper_one", warning_days=20, critical_days=30)
#        self.assertFormError(self.documentmodel_false)


    def test_create_empty_profile(self):
        self.logged_in = self.client.login(username="user_one", password="user_one")
        self.documentmodel_two = DocumentModel.objects.create(user_id=self.user_one, name="documentmodel_two", warning_days=10, critical_days=5)
        self.profile_two = Profile.objects.create(user_id=self.user_one, name="profile_two")
        self.profile_two.save()
        self.assertTrue(self.profile_two)


    def test_create_employee(self):
        self.logged_in = self.client.login(username="user_one", password="user_one")
        self.employee_one = Employee.objects.create(user_id=self.user_one, first_name="employee_one", last_name="employee_one", profile_id=self.profile_one)
        self.employee_one.save()
        self.assertTrue(self.employee_one)


    def test_update_documentmodel(self):
        self.logged_in = self.client.login(username="user_one", password="user_one")
        self.documentmodel_one_one.warning_days=300
        self.documentmodel_one_one.save()
        new_value = self.documentmodel_one_one.warning_days
        self.assertEqual(new_value, 300)

    # def test_create_complete_model(self):
    #     self.logged_in = self.client.login(username="user_one", password="user_one")
    #     self.documentmodel_fulltest = DocumentModel.objects.create(user_id=self.user_one, name="paper_fulltest", warning_days=10, critical_days=5)
    #     self.documentmodel_fulltest.save()
    #     self.documentmodel_list_fulltest = documentmodels_list.objects.create(user_id=self.user_one, profile_id=self.profile_fulltest, documentmodel=self.documentmodel_fulltest)
    #     self.documentmodel_list_fulltest.save()
    #     self.profile_fulltest = Profile.objects.create(user_id=self.user_one, name="profile_fulltest", documentmodels_list=[self.documentmodel_fulltest])
    #     self.profile_fulltest.save()
    #     self.employee_fulltest = Employee.objects.create(user_id=self.user_one, first_name="first_namefulltest",last_name="last_namefulltest", profile=self.profile_fulltest)
    #     self.employee_fulltest.save()
    #     self.assertTrue(self.employee_fulltest)
