# -*- coding: utf-8 -*-
from django import forms

from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ["user_id"]
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields["profile_id"].widget = forms.widgets.Select()
        self.fields["profile_id"].help_text = "Profile"
        self.fields["profile_id"].queryset = Profile.objects.all()
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


class ProfileForm (forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user_id"]
    def __init__ (self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["documentmodels_list"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["documentmodels_list"].help_text = "List of documents"
        self.fields["documentmodels_list"].queryset = DocumentModel.objects.all()


class DocumentModelForm(forms.Form):
    name = forms.CharField()
    warning_days = forms.CharField()
    critical_days = forms.CharField()
