# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class EmployeeForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    profile = forms.ChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"),
            ('option_two', "Option two can is something else and selecting it will deselect option one")
        ),
        widget = forms.RadioSelect,
        initial = 'option_two',
    )


class ProfileForm(forms.Form):
    name = forms.CharField()
    checkboxes = forms.MultipleChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"),
            ('option_two', 'Option two can also be checked and included in form results'),
            ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
        ),
        initial = 'option_one',
        widget = forms.CheckboxSelectMultiple,
        help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    )


class DocumentModelForm(forms.Form):
    name = forms.CharField()
    warning_days = forms.CharField()
    critical_days = forms.CharField()
