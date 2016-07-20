import datetime

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import AccountType, Employee, Profile, \
                    DocumentModel, Document


class CerbereAppViewsTestCase(TestCase):
    def setUp(self):
        #account_type = AccountType.objects.create(user_id=1, name="Silver")
        #self.user = User.objects.create_user(username="user_one", email="user_one@gmail.com", password="password_one", AccountType="Silver")
        pass

    def view_root(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def view_index(self):
        resp = self.client.get('/index/')
        self.assertEqual(resp.status_code, 200)

    def is_account_private(self):
        resp = self.client.get('/account/')
        self.assertEqual(resp.status_code, 302)

    def is_employee_private(self):
        resp = self.client.get('/employees/')
        self.assertEqual(resp.status_code, 302)

    def test_false_login(self):
        self.logged_in = self.client.login(username="user_one", password="password_two")
        self.assertFalse(self.logged_in)
        resp = self.client.get('/account/')


#class AccountsMethodTests(TestCase):
#    def account_creation_with_invalid_email(self):


#class EmployeesMethodTests(TestCase):
#    def employee_has_no_profile(self):
