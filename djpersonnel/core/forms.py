# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm


class ApproverForm(forms.Form):

    email = forms.EmailField(max_length=254)

    class Meta:
        fields = ['email']


class DateCreatedForm(forms.Form):

    created_at = forms.DateField(label="Created on or after")

    class Meta:
        pass
