# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponse, request
from django.contrib.auth.models import User, Group

from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class DocumentModelForm(forms.ModelForm):
    class Meta:
        model = DocumentModel
        fields = ["name","warning_days","critical_days"]
    def __init__(self, *args, **kwargs):
        super(DocumentModelForm, self).__init__(*args, **kwargs)
        self.fields["warning_days"].widget = forms.widgets.NumberInput()
        self.fields["warning_days"].help_text = "Number of warning days"
        self.fields["critical_days"].widget = forms.widgets.NumberInput()
        self.fields["critical_days"].help_text = "Number of critical days"
        #self.fields['user_id'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(DocumentModelForm, self).clean()
        warning_days = cleaned_data.get("warning_days")
        critical_days = cleaned_data.get("critical_days")

        if critical_days > warning_days:
            raise forms.ValidationError("Warning must be greater than critical.")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name","documentmodels_list"]
    def __init__ (self, *args, **kwargs):
        logged_user=kwargs.pop('logged_user')
        documentmodels = []
        for documentmodel in DocumentModel.objects.filter(user_id=logged_user):
            documentmodels.append((documentmodel.id, documentmodel.name))
        super(ProfileForm, self).__init__(*args, **kwargs)
        #self.fields['user_id'].widget = forms.HiddenInput()
        self.fields["documentmodels_list"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["documentmodels_list"].help_text = ""
        self.fields["documentmodels_list"].choices = documentmodels


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["user_id","first_name","last_name","is_active","profile_id"]
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].widget = forms.HiddenInput()
        self.fields["profile_id"].widget = forms.widgets.Select()
        self.fields["profile_id"].help_text = "Select the employee's profile"
        #self.fields["profile_id"].queryset = Profile.objects.all().filter(user_id=request.user)
        #self.fields["profile_id"].initial = Profile.objects.all()

    #first_name = forms.CharField(label=("first Name"), max_length=255)
    #last_name = forms.CharField()
    #profile = forms.ChoiceField(
    #    choices = (
    #        ('option_one', "Option one is this and that be sure to include why it's great"),
    #        ('option_two', "Option two can is something else and selecting it will deselect option one")
    #    ),
    #    widget = forms.RadioSelect,
    #    initial = 'option_two',
    #)
